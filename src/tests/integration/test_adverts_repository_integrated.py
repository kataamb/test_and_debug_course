import pytest
import uuid
from datetime import datetime, timezone, timedelta
from sqlalchemy.sql import text
from tests.fixtures.advert_builders import AdvertBuilder, AdvertMother
from tests.helpers import TestDataHelper

class TestAdvertsRepositoryIntegration:
    """Интеграционные тесты для AdvertsRepository с реальным SQL Builder"""
    
    @pytest.mark.asyncio
    async def test_create_advert_success(self, advert_repository, session):
        """Позитивный тест создания объявления"""
        # Arrange
        # Сначала создаем продавца
        seller_id = uuid.uuid4()
        profile_id = uuid.uuid4()
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller_id, "profile_id": profile_id}
        )
        await session.commit()
        
        # Создаем объявление с profile_id продавца
        advert = AdvertBuilder().with_user_id(profile_id).build()
        
        # Act
        created_advert = await advert_repository.create(advert)
        
        # Assert
        assert created_advert is not None
        assert created_advert.content == advert.content
        assert created_advert.description == advert.description
        assert created_advert.price == advert.price
        assert created_advert.id_seller == seller_id  # Должен быть id продавца, а не profile_id
        
        # Проверяем в БД
        result = await session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": created_advert.id}
        )
        assert result.scalar() == 1

    '''
    @pytest.mark.asyncio
    async def test_create_advert_seller_not_found(self, advert_repository):
        """Негативный тест: продавец не найден"""
        # Arrange
        advert = AdvertBuilder().with_user_id(uuid.uuid4()).build()
        
        # Act & Assert
        with pytest.raises((IntegrityError, SQLAlchemyError)):
            await advert_repository.create(advert)
    '''

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, advert_repository, session):
        """Позитивный тест получения объявления по ID"""
        # Arrange
        advert = await TestDataHelper.setup_test_advert(session, None)
        
        # Act
        retrieved_advert = await advert_repository.get_by_id(advert.id)
        
        # Assert
        assert retrieved_advert is not None
        assert retrieved_advert.id == advert.id
        assert retrieved_advert.content == advert.content
        assert retrieved_advert.description == advert.description
    
    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, advert_repository):
        """Негативный тест: объявление не найдено"""
        # Arrange
        non_existent_id = uuid.uuid4()
        
        # Act & Assert
        with pytest.raises(ValueError, match=f"Advert with id {non_existent_id} not found"):
            await advert_repository.get_by_id(non_existent_id)
    
    @pytest.mark.asyncio
    async def test_get_all_adverts(self, advert_repository, session):
        """Позитивный тест получения всех объявлений"""
        # Arrange
        advert1 = await TestDataHelper.setup_test_advert(session, None)
        advert2 = await TestDataHelper.setup_test_advert(session, None)
        
        # Act
        adverts = await advert_repository.get_all_adverts()
        
        # Assert
        assert len(adverts) >= 2
        ids = {advert.id for advert in adverts}
        assert advert1.id in ids
        assert advert2.id in ids
    
    @pytest.mark.asyncio
    async def test_get_advert_by_user(self, advert_repository, session):
        """Позитивный тест получения объявлений пользователя"""
        # Arrange
        profile_id = uuid.uuid4()
        seller1_id = uuid.uuid4()
        
        # Создаем продавца
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller1_id, "profile_id": profile_id}
        )
        
        # Создаем объявления для этого продавца
        advert1 = AdvertBuilder().with_user_id(profile_id).build()
        advert2 = AdvertBuilder().with_user_id(profile_id).build()
        
        await advert_repository.create(advert1)
        await advert_repository.create(advert2)
        
        # Создаем другое объявление для другого продавца
        seller2_id = uuid.uuid4()
        profile2_id = uuid.uuid4()
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller2_id, "profile_id": profile2_id}
        )
        advert3 = AdvertBuilder().with_user_id(profile2_id).build()
        await advert_repository.create(advert3)
        
        # Act
        user_adverts = await advert_repository.get_advert_by_user(profile_id)
        
        # Assert
        assert len(user_adverts) == 2
        for advert in user_adverts:
            assert advert.id_seller == seller1_id
    
    @pytest.mark.asyncio
    async def test_is_created_true(self, advert_repository, session):
        """Позитивный тест проверки существования объявления пользователя"""
        # Arrange
        profile_id = uuid.uuid4()
        seller_id = uuid.uuid4()
        
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller_id, "profile_id": profile_id}
        )
        
        advert = AdvertBuilder().with_user_id(profile_id).build()
        created_advert = await advert_repository.create(advert)
        
        # Act
        result = await advert_repository.is_created(profile_id, created_advert.id)
        
        # Assert
        assert result is True
    
    @pytest.mark.asyncio
    async def test_is_created_false(self, advert_repository, session):
        """Негативный тест: объявление не принадлежит пользователю"""
        # Arrange
        # Создаем продавца 1
        profile1_id = uuid.uuid4()
        seller1_id = uuid.uuid4()
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller1_id, "profile_id": profile1_id}
        )
        
        # Создаем объявление для продавца 1
        advert = AdvertBuilder().with_user_id(profile1_id).build()
        created_advert = await advert_repository.create(advert)
        
        # Создаем продавца 2
        profile2_id = uuid.uuid4()
        
        # Act
        result = await advert_repository.is_created(profile2_id, created_advert.id)
        
        # Assert
        assert result is False
    
    @pytest.mark.asyncio
    async def test_search_by_keyword(self, advert_repository, session):
        """Позитивный тест поиска по ключевому слову"""
        # Arrange
        seller_id = await TestDataHelper.setup_test_seller(session)
        
        # Создаем объявление с ключевым словом
        keyword = "специфичное_слово"
        advert = TestDataHelper.create_test_advert(
            seller_id, 
            content=f"Объявление с {keyword} в заголовке",
            description="Обычное описание"
        )
        
        await TestDataHelper.setup_test_advert(session, None, seller_id=seller_id, 
                                              content=advert.content, 
                                              description=advert.description)
        
        # Act
        found_adverts = await advert_repository.get_adverts_by_key_word(keyword)
        
        # Assert
        assert len(found_adverts) >= 1
        assert any(keyword in advert.content for advert in found_adverts)
    
    @pytest.mark.asyncio
    async def test_update_advert_full(self, advert_repository, session):
        """Позитивный тест полного обновления объявления"""
        # Arrange
        advert = await TestDataHelper.setup_test_advert(session, None)
        
        # Создаем обновленные данные
        updated_advert = AdvertBuilder()\
            .with_content("Обновленный заголовок")\
            .with_description("Обновленное описание")\
            .with_price(9999)\
            .with_category_id(uuid.uuid4())\
            .build()
        
        # Act
        result = await advert_repository.update_advert(advert.id, updated_advert)
        
        # Assert
        assert result is not None
        assert result.content == "Обновленный заголовок"
        assert result.description == "Обновленное описание"
        assert result.price == 9999
        
        # Проверяем в БД
        db_result = await session.execute(
            text("SELECT content FROM adv_uuid.adverts WHERE id = :id"),
            {"id": advert.id}
        )
        assert db_result.scalar() == "Обновленный заголовок"
    
    @pytest.mark.asyncio
    async def test_update_advert_partial(self, advert_repository, session):
        """Позитивный тест частичного обновления объявления"""
        # Arrange
        advert = await TestDataHelper.setup_test_advert(session, None)
        
        update_data = {
            "content": "Только заголовок обновлен",
            "price": 5000
        }
        
        # Act
        result = await advert_repository.partial_update_advert(advert.id, update_data)
        
        # Assert
        assert result is not None
        assert result.content == "Только заголовок обновлен"
        assert result.price == 5000
        # Проверяем, что другие поля не изменились
        assert result.description == advert.description
    
    @pytest.mark.asyncio
    async def test_update_advert_not_found(self, advert_repository):
        """Негативный тест: объявление для обновления не найдено"""
        # Arrange
        non_existent_id = uuid.uuid4()
        advert = AdvertMother.create_valid_advert()
        
        # Act & Assert
        with pytest.raises(ValueError):
            await advert_repository.update_advert(non_existent_id, advert)
    
    @pytest.mark.asyncio
    async def test_delete_advert_success(self, advert_repository, session):
        """Позитивный тест удаления объявления"""
        # Arrange
        profile_id = uuid.uuid4()
        seller_id = uuid.uuid4()
        
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller_id, "profile_id": profile_id}
        )
        
        advert = AdvertBuilder().with_user_id(profile_id).build()
        created_advert = await advert_repository.create(advert)
        
        # Act
        await advert_repository.delete_advert(created_advert.id, seller_id)
        
        # Assert
        result = await session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": created_advert.id}
        )
        assert result.scalar() == 0
    
    @pytest.mark.asyncio
    async def test_delete_advert_wrong_user(self, advert_repository, session):
        """Негативный тест: удаление объявления не своим пользователем"""
        # Arrange
        # Создаем продавца 1 и его объявление
        profile1_id = uuid.uuid4()
        seller1_id = uuid.uuid4()
        await session.execute(
            text("INSERT INTO adv_uuid.sellers (id, profile_id) VALUES (:id, :profile_id)"),
            {"id": seller1_id, "profile_id": profile1_id}
        )
        
        advert = AdvertBuilder().with_user_id(profile1_id).build()
        created_advert = await advert_repository.create(advert)
        
        # Создаем продавца 2
        seller2_id = uuid.uuid4()
        
        # Act
        await advert_repository.delete_advert(created_advert.id, seller2_id)
        
        # Assert - объявление должно остаться в БД
        result = await session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": created_advert.id}
        )
        assert result.scalar() == 1
    
    @pytest.mark.asyncio
    async def test_get_adverts_by_filter_dates(self, advert_repository, session):
        """Позитивный тест фильтрации по датам"""
        # Arrange
        now = datetime.now(timezone.utc)
        
        # Создаем объявления с разными датами
        seller_id = await TestDataHelper.setup_test_seller(session)
        
        # Объявление вчера
        yesterday_advert = TestDataHelper.create_test_advert(seller_id)
        await session.execute(
            text("""
                INSERT INTO adv_uuid.adverts 
                (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": yesterday_advert.id,
                "content": yesterday_advert.content,
                "description": yesterday_advert.description,
                "id_category": yesterday_advert.id_category,
                "price": yesterday_advert.price,
                "id_seller": seller_id,
                "date_created": now - timedelta(days=1)
            }
        )
        
        # Объявление сегодня
        today_advert = TestDataHelper.create_test_advert(seller_id)
        await session.execute(
            text("""
                INSERT INTO adv_uuid.adverts 
                (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": today_advert.id,
                "content": today_advert.content,
                "description": today_advert.description,
                "id_category": today_advert.id_category,
                "price": today_advert.price,
                "id_seller": seller_id,
                "date_created": now
            }
        )
        
        await session.commit()
        
        # Act - ищем объявления за последние 2 дня
        adverts = await advert_repository.get_adverts_by_filter(
            begin_time=now - timedelta(days=2),
            end_time=now
        )
        
        # Assert
        assert len(adverts) >= 2
        advert_ids = {advert.id for advert in adverts}
        assert yesterday_advert.id in advert_ids
        assert today_advert.id in advert_ids