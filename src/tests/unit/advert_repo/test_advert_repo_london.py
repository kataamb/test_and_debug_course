# tests/unit/advert_repo/test_advert_repo_london.py
import pytest
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from repositories.advert_repository import AdvertsRepository
from tests.resources.advert_test_data.builder_advert import AdvertBuilder


class TestAdvertRepositoryLondon:
    """Лондонские тесты для AdvertsRepository (полностью изолированные)"""

    @pytest.fixture
    def mock_session(self):
        """Асинхронный mock сессии"""
        session = AsyncMock()
        return session

    @pytest.fixture
    def mock_builder(self):
        """Строгий mock builder"""
        return MagicMock()

    @pytest.fixture
    def repository(self, mock_session, mock_builder):
        """Репозиторий с инжектированными mock зависимостями"""
        return AdvertsRepository(mock_session, mock_builder)

    @pytest.mark.asyncio
    async def test_create_calls_builder_with_correct_advert(self, repository, mock_builder, mock_session):
        """Тест проверяет вызов builder с правильным объявлением"""
        # Arrange
        advert = AdvertBuilder().build()
        sql = "INSERT INTO adverts ..."
        params = {}
        mock_builder.create.return_value = (sql, params)

        # Создаем моки для результата
        mock_result = MagicMock()  # Обычный MagicMock, не AsyncMock!
        mock_row = {"id": str(advert.id), "content": advert.content,
                    "description": advert.description, "id_category": str(advert.id_category),
                    "price": advert.price, "id_seller": str(advert.id_seller),
                    "date_created": advert.date_created}
        mock_mappings = MagicMock()
        mock_mappings.first.return_value = mock_row
        mock_result.mappings.return_value = mock_mappings

        # Настраиваем execute чтобы возвращал уже готовый результат (не корутину)
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.create(advert)

        # Assert
        mock_builder.create.assert_called_once_with(advert)
        assert result == advert  # Или проверьте правильность возвращаемого объекта

    @pytest.mark.asyncio
    async def test_create_calls_session_execute_with_correct_sql(self, repository, mock_builder, mock_session):
        """Тест проверяет вызов session.execute с правильным SQL"""
        # Arrange
        advert = AdvertBuilder().build()
        sql = "INSERT INTO adverts ..."
        params = {"id": str(advert.id)}
        mock_builder.create.return_value = (sql, params)

        mock_result = MagicMock()
        mock_row = {"id": str(advert.id), "content": advert.content,
                    "description": advert.description, "id_category": str(advert.id_category),
                    "price": advert.price, "id_seller": str(advert.id_seller),
                    "date_created": advert.date_created}
        mock_mappings = MagicMock()
        mock_mappings.first.return_value = mock_row
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        await repository.create(advert)

        # Assert
        mock_session.execute.assert_called_once_with(sql, params)

    @pytest.mark.asyncio
    async def test_create_calls_session_commit(self, repository, mock_builder, mock_session):
        """Тест проверяет вызов commit после успешного создания"""
        # Arrange
        advert = AdvertBuilder().build()
        sql = "INSERT INTO adverts ..."
        params = {}
        mock_builder.create.return_value = (sql, params)

        mock_result = MagicMock()
        mock_row = {"id": str(advert.id), "content": advert.content,
                    "description": advert.description, "id_category": str(advert.id_category),
                    "price": advert.price, "id_seller": str(advert.id_seller),
                    "date_created": advert.date_created}
        mock_mappings = MagicMock()
        mock_mappings.first.return_value = mock_row
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        await repository.create(advert)

        # Assert
        mock_session.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_create_calls_rollback_on_integrity_error(self, repository, mock_builder, mock_session):
        """Тест проверяет вызов rollback при ошибке целостности"""
        # Arrange
        advert = AdvertBuilder().build()
        sql = "INSERT INTO adverts ..."
        params = {}
        mock_builder.create.return_value = (sql, params)
        mock_session.execute.side_effect = IntegrityError("", "", "")

        # Act
        try:
            await repository.create(advert)
        except IntegrityError:
            pass

        # Assert
        mock_session.rollback.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_get_by_id_calls_builder_with_correct_id(self, repository, mock_builder, mock_session):
        """Тест проверяет передачу правильного ID в builder"""
        # Arrange
        advert_id = UUID(int=1)
        sql = "SELECT * FROM adverts WHERE id = :id"
        params = {"id": str(advert_id)}
        mock_builder.get_by_id.return_value = (sql, params)

        mock_result = MagicMock()
        mock_row = {"id": str(advert_id), "content": "test",
                    "description": "desc", "id_category": str(UUID(int=1)),
                    "price": 100, "id_seller": str(UUID(int=1)),
                    "date_created": AdvertBuilder().build().date_created}
        mock_mappings = MagicMock()
        mock_mappings.first.return_value = mock_row
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_by_id(advert_id)

        # Assert
        mock_builder.get_by_id.assert_called_once_with(advert_id)
        assert result is not None

    @pytest.mark.asyncio
    async def test_get_all_adverts_calls_builder_once(self, repository, mock_builder, mock_session):
        """Тест проверяет однократный вызов builder"""
        # Arrange
        sql = "SELECT * FROM adverts"
        params = {}
        mock_builder.get_all.return_value = (sql, params)

        mock_result = MagicMock()
        # Для get_all_adverts нужно настроить mappings чтобы возвращал итерируемый объект
        mock_row1 = {"id": str(UUID(int=1)), "content": "test1",
                     "description": "desc1", "id_category": str(UUID(int=1)),
                     "price": 100, "id_seller": str(UUID(int=1)),
                     "date_created": AdvertBuilder().build().date_created}
        mock_row2 = {"id": str(UUID(int=2)), "content": "test2",
                     "description": "desc2", "id_category": str(UUID(int=2)),
                     "price": 200, "id_seller": str(UUID(int=2)),
                     "date_created": AdvertBuilder().build().date_created}

        mock_mappings = MagicMock()
        mock_mappings.return_value = [mock_row1, mock_row2]  # Возвращаем список, а не корутину
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_all_adverts()

        # Assert
        mock_builder.get_all.assert_called_once()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_advert_by_user_calls_builder_with_correct_user_id(self, repository, mock_builder, mock_session):
        """Тест проверяет передачу правильного user_id в builder"""
        # Arrange
        user_id = UUID(int=1)
        sql = "SELECT * FROM adverts WHERE id_seller = :user_id"
        params = {"user_id": str(user_id)}
        mock_builder.get_by_user.return_value = (sql, params)

        mock_result = MagicMock()
        mock_row = {"id": str(UUID(int=1)), "content": "test",
                    "description": "desc", "id_category": str(UUID(int=1)),
                    "price": 100, "id_seller": str(user_id),
                    "date_created": AdvertBuilder().build().date_created}

        mock_mappings = MagicMock()
        mock_mappings.return_value = [mock_row]  # Возвращаем список
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_advert_by_user(user_id)

        # Assert
        mock_builder.get_by_user.assert_called_once_with(user_id)
        assert len(result) == 1

    # tests/unit/advert_repo/test_advert_repo_london.py

    @pytest.mark.asyncio
    async def test_get_all_adverts_calls_builder_once(self, repository, mock_builder, mock_session):
        """Тест проверяет однократный вызов builder"""
        # Arrange
        sql = "SELECT * FROM adverts"
        params = {}
        mock_builder.get_all.return_value = (sql, params)

        # Создаем моки для результата
        mock_result = MagicMock()

        # Настраиваем mappings правильно
        mock_row1 = {"id": str(UUID(int=1)), "content": "test1",
                     "description": "desc1", "id_category": str(UUID(int=1)),
                     "price": 100, "id_seller": str(UUID(int=1)),
                     "date_created": AdvertBuilder().build().date_created}
        mock_row2 = {"id": str(UUID(int=2)), "content": "test2",
                     "description": "desc2", "id_category": str(UUID(int=2)),
                     "price": 200, "id_seller": str(UUID(int=2)),
                     "date_created": AdvertBuilder().build().date_created}

        # Вариант 1: mappings() возвращает итерируемый объект
        mock_mappings = MagicMock()
        mock_mappings.__iter__.return_value = iter([mock_row1, mock_row2])
        # ИЛИ просто сделать mock_mappings списком
        # mock_mappings = [mock_row1, mock_row2]

        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_all_adverts()

        # Assert
        mock_builder.get_all.assert_called_once()
        assert len(result) == 2
        # Дополнительные проверки если нужно
        assert result[0].content == "test1"
        assert result[1].content == "test2"

    @pytest.mark.asyncio
    async def test_get_advert_by_user_calls_builder_with_correct_user_id(self, repository, mock_builder, mock_session):
        """Тест проверяет передачу правильного user_id в builder"""
        # Arrange
        user_id = UUID(int=1)
        sql = "SELECT * FROM adverts WHERE id_seller = :user_id"
        params = {"user_id": str(user_id)}
        mock_builder.get_by_user.return_value = (sql, params)

        # Создаем моки для результата
        mock_result = MagicMock()

        mock_row = {"id": str(UUID(int=1)), "content": "test",
                    "description": "desc", "id_category": str(UUID(int=1)),
                    "price": 100, "id_seller": str(user_id),
                    "date_created": AdvertBuilder().build().date_created}

        # mappings() должен возвращать итерируемый объект
        mock_mappings = MagicMock()
        mock_mappings.__iter__.return_value = iter([mock_row])
        mock_result.mappings.return_value = mock_mappings
        mock_session.execute.return_value = mock_result

        # Act
        result = await repository.get_advert_by_user(user_id)

        # Assert
        mock_builder.get_by_user.assert_called_once_with(user_id)
        assert len(result) == 1
        assert result[0].id_seller == user_id