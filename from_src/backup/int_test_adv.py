"""
Интеграционные тесты для AdvertsRepository (classic-style с реальной БД)
"""

import pytest
import uuid
from datetime import datetime, timedelta
from sqlalchemy import text

from models.advert import Advert
from tests.fixtures.advert_builders import AdvertBuilder, AdvertMother


class TestAdvertsRepositoryIntegration:
    """Test suite для AdvertsRepository (интеграционные тесты)"""

    # ==================== HELPER METHODS ====================

    async def create_seller(self, db_session, profile_id: uuid.UUID) -> uuid.UUID:
        """Создает seller и возвращает его id"""
        result = await db_session.execute(
            text("""
                INSERT INTO adv_uuid.sellers (profile_id)
                VALUES (:profile_id)
                RETURNING id
            """),
            {"profile_id": str(profile_id)}
        )
        seller_row = result.first()
        if seller_row:
            return seller_row[0]

        # Если seller уже существует, получаем его id
        result = await db_session.execute(
            text("SELECT id FROM adv_uuid.sellers WHERE profile_id = :profile_id"),
            {"profile_id": str(profile_id)}
        )
        existing = result.first()
        return existing[0] if existing else None

    async def create_advert_directly(self, db_session, advert: Advert, seller_profile_id: uuid.UUID = None):
        """Создает объявление напрямую в БД"""
        if seller_profile_id is None:
            seller_profile_id = advert.id_seller

        # Получаем или создаем seller
        seller_id = await self.create_seller(db_session, seller_profile_id)

        # Создаем advert
        await db_session.execute(
            text("""
                INSERT INTO adv_uuid.adverts (id, content, description, price, id_category, id_seller)
                VALUES (:id, :content, :description, :price, :id_category, :seller_id)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "price": advert.price,
                "id_category": str(advert.id_category),
                "seller_id": seller_id
            }
        )
        await db_session.commit()
        return advert.id

    # ==================== CREATE METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_create_integration_success(self, repository_integration, db_session):
        """Позитивный тест: успешное создание объявления"""
        # Arrange
        advert = AdvertMother.create_valid_advert()

        # Создаем seller в БД
        await self.create_seller(db_session, advert.id_seller)

        # Act
        result = await repository_integration.create(advert)

        # Assert
        assert result is not None
        assert isinstance(result, Advert)
        assert result.content == advert.content
        assert result.price == advert.price

        # Проверяем, что действительно сохранено в БД
        db_result = await db_session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": str(result.id)}
        )
        count = db_result.scalar()
        assert count == 1

    @pytest.mark.asyncio
    async def test_create_integration_missing_seller(self, repository_integration):
        """Негативный тест: создание без seller (ожидаем ошибку)"""
        # Arrange
        advert = AdvertMother.create_valid_advert()
        # НЕ создаем seller

        # Act & Assert
        # Должна быть ошибка внешнего ключа
        with pytest.raises(Exception):
            await repository_integration.create(advert)

    # ==================== GET_BY_ID METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_get_by_id_integration_success(self, repository_integration, db_session, sample_uuid):
        """Позитивный тест: успешное получение объявления по ID"""
        # Arrange
        advert = AdvertBuilder() \
            .with_content("Test Get By ID") \
            .with_price(2500) \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert)

        # Act
        result = await repository_integration.get_by_id(advert_id)

        # Assert
        assert isinstance(result, Advert)
        assert result.id == advert_id
        assert result.content == "Test Get By ID"
        assert result.price == 2500

    @pytest.mark.asyncio
    async def test_get_by_id_integration_not_found(self, repository_integration):
        """Негативный тест: объявление не найдено"""
        # Arrange
        non_existent_id = uuid.uuid4()

        # Act & Assert
        with pytest.raises(ValueError, match=f"Advert with id {non_existent_id} not found"):
            await repository_integration.get_by_id(non_existent_id)

    # ==================== GET_ALL_ADVERTS METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_get_all_adverts_integration(self, repository_integration, db_session):
        """Позитивный тест: получение всех объявлений"""
        # Arrange - создаем несколько объявлений
        advert_ids = []
        for i in range(3):
            advert = AdvertBuilder() \
                .with_content(f"Test Advert {i}") \
                .with_price(100 * (i + 1)) \
                .build()

            advert_id = await self.create_advert_directly(db_session, advert)
            advert_ids.append(advert_id)

        # Act
        result = await repository_integration.get_all_adverts()

        # Assert
        assert isinstance(result, list)
        assert len(result) >= 3
        assert all(isinstance(adv, Advert) for adv in result)

        # Проверяем, что наши объявления есть в результате
        result_ids = [adv.id for adv in result]
        for advert_id in advert_ids:
            assert advert_id in result_ids

    # ==================== GET_ADVERT_BY_USER METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_get_advert_by_user_integration(self, repository_integration, db_session):
        """Позитивный тест: получение объявлений пользователя"""
        # Arrange
        user1_id = uuid.uuid4()
        user2_id = uuid.uuid4()

        # Создаем seller для пользователей
        await self.create_seller(db_session, user1_id)
        await self.create_seller(db_session, user2_id)

        # Создаем объявления для user1
        advert1 = AdvertBuilder() \
            .with_user_id(user1_id) \
            .with_content("User1 Advert 1") \
            .build()

        advert2 = AdvertBuilder() \
            .with_user_id(user1_id) \
            .with_content("User1 Advert 2") \
            .build()

        # Создаем объявление для user2
        advert3 = AdvertBuilder() \
            .with_user_id(user2_id) \
            .with_content("User2 Advert") \
            .build()

        await self.create_advert_directly(db_session, advert1, user1_id)
        await self.create_advert_directly(db_session, advert2, user1_id)
        await self.create_advert_directly(db_session, advert3, user2_id)

        # Act
        result = await repository_integration.get_advert_by_user(user1_id)

        # Assert
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(adv, Advert) for adv in result)
        assert all(adv.content.startswith("User1") for adv in result)

    # ==================== IS_CREATED METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_is_created_integration_true(self, repository_integration, db_session):
        """Позитивный тест: проверка, что объявление создано пользователем"""
        # Arrange
        user_id = uuid.uuid4()
        advert = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Is Created Test") \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user_id)

        # Act
        result = await repository_integration.is_created(user_id, advert_id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_is_created_integration_false(self, repository_integration, db_session):
        """Позитивный тест: проверка, что объявление НЕ создано пользователем"""
        # Arrange
        user1_id = uuid.uuid4()
        user2_id = uuid.uuid4()

        advert = AdvertBuilder() \
            .with_user_id(user1_id) \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user1_id)

        # Act - проверяем от другого пользователя
        result = await repository_integration.is_created(user2_id, advert_id)

        # Assert
        assert result is False

    # ==================== UPDATE METHODS TESTS ====================

    @pytest.mark.asyncio
    async def test_update_advert_integration(self, repository_integration, db_session):
        """Интеграционный тест: полное обновление объявления"""
        # Arrange
        user_id = uuid.uuid4()
        advert = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Original Content") \
            .with_price(1000) \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user_id)

        # Создаем обновленную версию
        updated_advert = AdvertBuilder() \
            .with_id(advert_id) \
            .with_content("Updated Content") \
            .with_description("Updated Description") \
            .with_price(9999) \
            .with_category_id(uuid.uuid4()) \
            .with_user_id(user_id) \
            .build()

        # Act
        result = await repository_integration.update_advert(advert_id, updated_advert)

        # Assert
        assert result is not None
        assert result.content == "Updated Content"
        assert result.price == 9999

        # Проверяем в БД
        db_result = await db_session.execute(
            text("SELECT content, price FROM adv_uuid.adverts WHERE id = :id"),
            {"id": str(advert_id)}
        )
        row = db_result.first()
        assert row[0] == "Updated Content"
        assert row[1] == 9999

    @pytest.mark.asyncio
    async def test_update_nonexistent_advert(self, repository_integration):
        """Негативный тест: обновление несуществующего объявления"""
        # Arrange
        non_existent_id = uuid.uuid4()
        advert = AdvertMother.create_valid_advert()

        # Act & Assert
        with pytest.raises(ValueError, match=f"Advert with id {non_existent_id} not found"):
            await repository_integration.update_advert(non_existent_id, advert)

    @pytest.mark.asyncio
    async def test_partial_update_integration(self, repository_integration, db_session, sample_update_data):
        """Интеграционный тест: частичное обновление"""
        # Arrange
        user_id = uuid.uuid4()
        advert = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Original") \
            .with_description("Original Description") \
            .with_price(1000) \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user_id)

        update_data = sample_update_data

        # Act
        result = await repository_integration.partial_update_advert(advert_id, update_data)

        # Assert
        assert result is not None
        assert result.content == update_data["content"]
        assert result.price == update_data["price"]
        # Описание должно остаться прежним (не обновляли)
        assert result.description == "Original Description"

    # ==================== DELETE METHOD TESTS ====================

    @pytest.mark.asyncio
    async def test_delete_advert_integration(self, repository_integration, db_session):
        """Интеграционный тест: успешное удаление объявления"""
        # Arrange
        user_id = uuid.uuid4()
        advert = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("To Delete") \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user_id)

        # Проверяем, что объявление существует
        check_result = await db_session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": str(advert_id)}
        )
        assert check_result.scalar() == 1

        # Act
        await repository_integration.delete_advert(advert_id, user_id)

        # Assert - проверяем что объявление удалено
        result = await db_session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": str(advert_id)}
        )
        count = result.scalar()
        assert count == 0

    @pytest.mark.asyncio
    async def test_delete_advert_wrong_user(self, repository_integration, db_session):
        """Интеграционный тест: удаление не своим пользователем"""
        # Arrange
        user1_id = uuid.uuid4()
        user2_id = uuid.uuid4()

        advert = AdvertBuilder() \
            .with_user_id(user1_id) \
            .with_content("Not Your Advert") \
            .build()

        advert_id = await self.create_advert_directly(db_session, advert, user1_id)

        # Act - пытаемся удалить другим пользователем
        await repository_integration.delete_advert(advert_id, user2_id)

        # Assert - объявление НЕ должно быть удалено
        result = await db_session.execute(
            text("SELECT COUNT(*) FROM adv_uuid.adverts WHERE id = :id"),
            {"id": str(advert_id)}
        )
        count = result.scalar()
        assert count == 1  # Все еще существует

    # ==================== SEARCH METHODS TESTS ====================

    @pytest.mark.asyncio
    async def test_get_adverts_by_key_word_integration(self, repository_integration, db_session):
        """Интеграционный тест: поиск по ключевому слову"""
        # Arrange
        user_id = uuid.uuid4()

        # Создаем объявления с разным содержанием
        advert1 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Продам ноутбук Dell") \
            .build()

        advert2 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Куплю MacBook") \
            .build()

        advert3 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Продам iPhone") \
            .build()

        await self.create_advert_directly(db_session, advert1, user_id)
        await self.create_advert_directly(db_session, advert2, user_id)
        await self.create_advert_directly(db_session, advert3, user_id)

        # Act - ищем "ноутбук"
        result = await repository_integration.get_adverts_by_key_word("ноутбук")

        # Assert
        assert isinstance(result, list)
        # Должно найти хотя бы одно объявление
        assert len(result) >= 1

        # Проверяем, что в результатах есть искомое слово
        for adv in result:
            assert "ноутбук" in adv.content.lower()

    @pytest.mark.asyncio
    async def test_get_adverts_by_filter_integration(self, repository_integration, db_session):
        """Интеграционный тест: фильтрация по датам"""
        # Arrange
        user_id = uuid.uuid4()

        # Создаем объявление с вчерашней датой
        yesterday = datetime.now() - timedelta(days=1)
        advert = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_content("Yesterday Advert") \
            .with_date_created(yesterday) \
            .build()

        await self.create_advert_directly(db_session, advert, user_id)

        # Создаем диапазон дат (сегодня минус 2 дня - сегодня)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=2)

        # Act
        result = await repository_integration.get_adverts_by_filter(start_date, end_date)

        # Assert
        assert isinstance(result, list)
        # Должно найти наше объявление
        assert any(adv.content == "Yesterday Advert" for adv in result)

    # ==================== CATEGORY METHODS TESTS ====================

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_integration(self, repository_integration, db_session):
        """Интеграционный тест: поиск по категории"""
        # Arrange
        user_id = uuid.uuid4()
        category1_id = uuid.uuid4()
        category2_id = uuid.uuid4()

        # Создаем объявления в разных категориях
        advert1 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_category_id(category1_id) \
            .with_content("Category 1 Advert") \
            .build()

        advert2 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_category_id(category2_id) \
            .with_content("Category 2 Advert") \
            .build()

        await self.create_advert_directly(db_session, advert1, user_id)
        await self.create_advert_directly(db_session, advert2, user_id)

        # Act - ищем по первой категории
        result = await repository_integration.get_adverts_by_category(category1_id)

        # Assert
        assert isinstance(result, list)
        assert len(result) >= 1
        assert all(adv.id_category == category1_id for adv in result)


    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_integration(self, repository_integration, db_session):
        """Интеграционный тест: поиск по категории и ключевому слову"""
        # Arrange
        user_id = uuid.uuid4()
        category_id = uuid.uuid4()

        # Создаем объявления
        advert1 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_category_id(category_id) \
            .with_content("Продам ноутбук Dell") \
            .build()

        advert2 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_category_id(category_id) \
            .with_content("Продам MacBook Pro") \
            .build()

        advert3 = AdvertBuilder() \
            .with_user_id(user_id) \
            .with_category_id(uuid.uuid4()) \
        .with_content("Продам ноутбук ASUS") \
            .build()

        await self.create_advert_directly(db_session, advert1, user_id)
        await self.create_advert_directly(db_session, advert2, user_id)
        await self.create_advert_directly(db_session, advert3, user_id)

        # Act - ищем "ноутбук" в определенной категории
        result = await repository_integration.get_adverts_by_category_and_keyword("ноутбук", category_id)

        # Assert
        assert isinstance(result, list)
        # Должно найти только advert1 (ноутбук Dell в нужной категории)
        assert len(result) == 1
        assert result[0].content == "Продам ноутбук Dell"

# ==================== DATA BUILDER AND OBJECT MOTHER TESTS ====================

@pytest.mark.asyncio
async def test_with_data_builder_integration(self, repository_integration, db_session):
    """Тест с использованием Data Builder"""
    # Arrange
    advert = AdvertBuilder() \
        .with_content("Builder Integration Test") \
        .with_description("Built with AdvertBuilder for integration") \
        .with_price(7777) \
        .with_category_id(uuid.uuid4()) \
        .with_user_id(uuid.uuid4()) \
        .build()

    # Создаем seller
    await self.create_seller(db_session, advert.id_seller)

    # Act
    result = await repository_integration.create(advert)

    # Assert
    assert result.content == "Builder Integration Test"
    assert result.price == 7777
    assert result.description == "Built with AdvertBuilder for integration"


@pytest.mark.asyncio
async def test_with_object_mother_integration(self, repository_integration, db_session):
    """Тест с использованием Object Mother"""
    # Arrange
    advert = AdvertMother.create_expensive_advert()

    # Создаем seller
    await self.create_seller(db_session, advert.id_seller)

    # Act
    result = await repository_integration.create(advert)

    # Assert
    assert result.price >= 10000  # Дорогое объявление

    # Проверяем через Object Mother для дешевого объявления
    cheap_advert = AdvertMother.create_cheap_advert()
    await self.create_seller(db_session, cheap_advert.id_seller)
    cheap_result = await repository_integration.create(cheap_advert)
    assert cheap_result.price <= 500  # Дешевое объявление
