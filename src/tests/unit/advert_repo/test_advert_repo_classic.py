# tests/unit/advert_repo/test_advert_repo_classic.py
import pytest
from uuid import UUID
from sqlalchemy import text
from repositories.advert_repository import AdvertsRepository
from tests.resources.advert_test_data.builder_advert import AdvertBuilder
from tests.resources.advert_test_data.mother_object_advert import MotherAdvert
from tests.fixtures.sqlite_sql_builders import SQLiteAdvertSqlBuilder


class TestAdvertRepositoryClassic:
    """Классические тесты для AdvertsRepository с реальной SQLite БД"""

    @pytest.fixture
    async def repository(self, db_session, setup_test_data):
        """Фикстура для создания репозитория с реальной БД"""
        builder = SQLiteAdvertSqlBuilder()
        return AdvertsRepository(db_session, builder)

    @pytest.fixture
    def sample_advert(self, setup_test_data):
        """Фикстура для тестового объявления"""
        test_data = setup_test_data
        return AdvertBuilder().with_id(1).with_category_id(test_data["category_id"]).with_seller(
            test_data["seller_id"]).build()

    @pytest.mark.asyncio
    async def test_create_advert_success(self, repository, db_session, sample_advert):
        """Позитивный тест создания объявления"""
        # Act
        result = await repository.create(sample_advert)

        # Assert
        assert result is not None
        assert result.id == sample_advert.id
        assert result.content == sample_advert.content
        assert result.description == sample_advert.description

        # Проверяем, что объявление действительно создано в БД
        check_result = await db_session.execute(
            text("SELECT * FROM adverts WHERE id = :id"),
            {"id": str(sample_advert.id)}
        )
        row = check_result.mappings().first()
        assert row is not None
        assert row["content"] == sample_advert.content

    @pytest.mark.asyncio
    async def test_get_by_id_success(self, repository, db_session, sample_advert):
        """Позитивный тест получения объявления по ID"""
        # Arrange - создаем объявление в БД
        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(sample_advert.id),
                "content": sample_advert.content,
                "description": sample_advert.description,
                "id_category": str(sample_advert.id_category),
                "price": sample_advert.price,
                "id_seller": str(sample_advert.id_seller),
                "date_created": sample_advert.date_created
            }
        )
        await db_session.commit()

        # Act
        result = await repository.get_by_id(sample_advert.id)

        # Assert
        assert result is not None
        assert result.id == sample_advert.id
        assert result.content == sample_advert.content

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository):
        """Негативный тест получения несуществующего объявления"""
        # Arrange
        non_existent_id = UUID(int=999)

        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await repository.get_by_id(non_existent_id)

    @pytest.mark.asyncio
    async def test_get_all_adverts_success(self, repository, db_session, setup_test_data):
        """Позитивный тест получения всех объявлений"""
        # Arrange - создаем несколько объявлений
        test_data = setup_test_data
        adverts = [
            AdvertBuilder().with_id(1).with_category_id(test_data["category_id"]).with_seller(
                test_data["seller_id"]).build(),
            AdvertBuilder().with_id(2).with_category_id(test_data["category_id"]).with_seller(
                test_data["seller_id"]).build()
        ]

        for advert in adverts:
            await db_session.execute(
                text("""
                    INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                    VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
                """),
                {
                    "id": str(advert.id),
                    "content": advert.content,
                    "description": advert.description,
                    "id_category": str(advert.id_category),
                    "price": advert.price,
                    "id_seller": str(advert.id_seller),
                    "date_created": advert.date_created
                }
            )
        await db_session.commit()

        # Act
        result = await repository.get_all_adverts()

        # Assert
        assert len(result) >= 2
        assert any(a.id == adverts[0].id for a in result)
        assert any(a.id == adverts[1].id for a in result)

    @pytest.mark.asyncio
    async def test_get_advert_by_user_success(self, repository, db_session, setup_test_data):
        """Позитивный тест получения объявлений пользователя"""
        # Arrange
        test_data = setup_test_data
        advert = AdvertBuilder().with_id(1).with_category_id(test_data["category_id"]).with_seller(
            test_data["seller_id"]).build()

        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "id_category": str(advert.id_category),
                "price": advert.price,
                "id_seller": str(advert.id_seller),
                "date_created": advert.date_created
            }
        )
        await db_session.commit()

        # Act - используем seller_id, так как в SQLite builder get_by_user ищет по id_seller
        result = await repository.get_advert_by_user(test_data["seller_id"])

        # Assert
        assert len(result) >= 1
        assert any(a.id == advert.id for a in result)

    @pytest.mark.asyncio
    async def test_is_created_true(self, repository, db_session, setup_test_data):
        """Позитивный тест проверки создания объявления пользователем"""
        # Arrange
        test_data = setup_test_data
        advert = AdvertBuilder().with_id(1).with_category_id(test_data["category_id"]).with_seller(
            test_data["seller_id"]).build()

        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "id_category": str(advert.id_category),
                "price": advert.price,
                "id_seller": str(advert.id_seller),
                "date_created": advert.date_created
            }
        )
        await db_session.commit()

        # Act - используем seller_id, так как в SQLite builder is_created ищет по id_seller
        result = await repository.is_created(test_data["seller_id"], advert.id)

        # Assert
        assert result is True

    @pytest.mark.asyncio
    async def test_is_created_false(self, repository, setup_test_data):
        """Негативный тест проверки создания объявления пользователем"""
        # Arrange
        test_data = setup_test_data
        non_existent_id = UUID(int=999)

        # Act
        result = await repository.is_created(test_data["user_id"], non_existent_id)

        # Assert
        assert result is False

    @pytest.mark.asyncio
    async def test_get_adverts_by_key_word_success(self, repository, db_session, setup_test_data):
        """Позитивный тест поиска по ключевому слову"""
        # Arrange
        test_data = setup_test_data
        advert = AdvertBuilder().with_id(1).with_content("smartphone").with_category_id(
            test_data["category_id"]).with_seller(test_data["seller_id"]).build()

        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "id_category": str(advert.id_category),
                "price": advert.price,
                "id_seller": str(advert.id_seller),
                "date_created": advert.date_created
            }
        )
        await db_session.commit()

        # Act
        result = await repository.get_adverts_by_key_word("smartphone")

        # Assert
        assert len(result) >= 1
        assert any("smartphone" in a.content.lower() for a in result)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_success(self, repository, db_session, setup_test_data):
        """Позитивный тест поиска по категории"""
        # Arrange
        test_data = setup_test_data
        advert = AdvertBuilder().with_id(1).with_category_id(test_data["category_id"]).with_seller(
            test_data["seller_id"]).build()

        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "id_category": str(advert.id_category),
                "price": advert.price,
                "id_seller": str(advert.id_seller),
                "date_created": advert.date_created
            }
        )
        await db_session.commit()

        # Act
        result = await repository.get_adverts_by_category(test_data["category_id"])

        # Assert
        assert len(result) >= 1
        assert any(a.id_category == test_data["category_id"] for a in result)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_success(self, repository, db_session, setup_test_data):
        """Позитивный тест поиска по категории и ключевому слову"""
        # Arrange
        test_data = setup_test_data
        advert = AdvertBuilder().with_id(1).with_content("smartphone").with_category_id(
            test_data["category_id"]).with_seller(test_data["seller_id"]).build()

        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(advert.id),
                "content": advert.content,
                "description": advert.description,
                "id_category": str(advert.id_category),
                "price": advert.price,
                "id_seller": str(advert.id_seller),
                "date_created": advert.date_created
            }
        )
        await db_session.commit()

        # Act
        result = await repository.get_adverts_by_category_and_keyword("smartphone", test_data["category_id"])

        # Assert
        assert len(result) >= 1
        assert any(a.id_category == test_data["category_id"] and "smartphone" in a.content.lower() for a in result)

    @pytest.mark.asyncio
    async def test_update_advert_success(self, repository, db_session, sample_advert):
        """Позитивный тест полного обновления объявления"""
        # Arrange - создаем объявление
        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(sample_advert.id),
                "content": sample_advert.content,
                "description": sample_advert.description,
                "id_category": str(sample_advert.id_category),
                "price": sample_advert.price,
                "id_seller": str(sample_advert.id_seller),
                "date_created": sample_advert.date_created
            }
        )
        await db_session.commit()

        # Обновляем объявление
        updated_advert = AdvertBuilder().with_id(1).with_content("Updated Content").build()
        updated_advert.id_category = sample_advert.id_category
        updated_advert.id_seller = sample_advert.id_seller

        # Act
        result = await repository.update_advert(sample_advert.id, updated_advert)

        # Assert
        assert result.content == "Updated Content"

        # Проверяем в БД
        check_result = await db_session.execute(
            text("SELECT * FROM adverts WHERE id = :id"),
            {"id": str(sample_advert.id)}
        )
        row = check_result.mappings().first()
        assert row["content"] == "Updated Content"

    @pytest.mark.asyncio
    async def test_update_advert_not_found(self, repository, sample_advert):
        """Негативный тест обновления несуществующего объявления"""
        # Arrange
        non_existent_id = UUID(int=999)

        # Act & Assert
        with pytest.raises(ValueError, match="not found"):
            await repository.update_advert(non_existent_id, sample_advert)

    @pytest.mark.asyncio
    async def test_partial_update_advert_success(self, repository, db_session, sample_advert):
        """Позитивный тест частичного обновления объявления"""
        # Arrange - создаем объявление
        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(sample_advert.id),
                "content": sample_advert.content,
                "description": sample_advert.description,
                "id_category": str(sample_advert.id_category),
                "price": sample_advert.price,
                "id_seller": str(sample_advert.id_seller),
                "date_created": sample_advert.date_created
            }
        )
        await db_session.commit()

        update_data = {
            "content": "Updated Content",
            "price": "25000"
        }

        # Act
        result = await repository.partial_update_advert(sample_advert.id, update_data)

        # Assert
        assert result.content == "Updated Content"

    @pytest.mark.asyncio
    async def test_delete_advert_success(self, repository, db_session, sample_advert, setup_test_data):
        """Позитивный тест удаления объявления"""
        # Arrange - создаем объявление
        await db_session.execute(
            text("""
                INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": str(sample_advert.id),
                "content": sample_advert.content,
                "description": sample_advert.description,
                "id_category": str(sample_advert.id_category),
                "price": sample_advert.price,
                "id_seller": str(sample_advert.id_seller),
                "date_created": sample_advert.date_created
            }
        )
        await db_session.commit()

        # Act
        await repository.delete_advert(sample_advert.id, setup_test_data["seller_id"])

        # Assert - проверяем, что объявление удалено
        check_result = await db_session.execute(
            text("SELECT * FROM adverts WHERE id = :id"),
            {"id": str(sample_advert.id)}
        )
        row = check_result.mappings().first()
        assert row is None
