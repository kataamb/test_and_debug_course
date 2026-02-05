# tests/unit/service/advert_service_london_test.py
import pytest
import asyncio
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock, patch
from services.advert_service import AdvertService
from models.advert import Advert
from api_v1.dto.advert_dto import AdvertUpdatePartialDTO
from tests.resources.advert_test_data.builder_advert import AdvertBuilder
from tests.resources.advert_test_data.mother_object_advert import MotherAdvert


class TestAdvertServiceLondon:
    """Лондонские тесты для AdvertService (полностью изолированные)"""

    @pytest.fixture
    def mock_repo(self):
        """Строгий mock репозитория"""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Сервис с инжектированным mock репозитория"""
        return AdvertService(mock_repo)

    @pytest.mark.asyncio
    async def test_create_advert_calls_repository(self, service, mock_repo):
        """Тест проверяет вызов репозитория с правильными аргументами"""
        # Arrange
        advert = AdvertBuilder().build()
        mock_repo.create.return_value = advert

        # Act
        await service.create_advert(advert)

        # Assert
        mock_repo.create.assert_called_once_with(advert)

    @pytest.mark.asyncio
    async def test_get_advert_calls_repository_with_correct_id(self, service, mock_repo):
        """Тест проверяет передачу правильного ID в репозиторий"""
        # Arrange
        advert_id = UUID(int=1)

        # Act
        await service.get_advert(advert_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)

    @pytest.mark.asyncio
    async def test_get_all_adverts_calls_repository_once(self, service, mock_repo):
        """Тест проверяет однократный вызов репозитория"""
        # Act
        await service.get_all_adverts()

        # Assert
        mock_repo.get_all_adverts.assert_called_once()

    @pytest.mark.asyncio
    async def test_is_created_calls_repository_with_correct_params(self, service, mock_repo):
        """Тест проверяет передачу правильных параметров"""
        # Arrange
        user_id = UUID(int=1)
        advert_id = UUID(int=1)

        # Act
        await service.is_created(user_id, advert_id)

        # Assert
        mock_repo.is_created.assert_called_once_with(user_id, advert_id)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_calls_correct_method(self, service, mock_repo):
        """Тест проверяет выбор правильного метода репозитория"""
        # Arrange
        keyword = "test"
        category_id = UUID(int=1)

        # Act
        await service.get_adverts_by_category_and_keyword(keyword, category_id)

        # Assert
        mock_repo.get_adverts_by_category_and_keyword.assert_called_once_with(keyword, category_id)

    @pytest.mark.asyncio
    async def test_partial_update_converts_dto_to_dict(self, service, mock_repo):
        """Тест проверяет преобразование DTO в словарь"""
        # Arrange
        advert_id = UUID(int=1)
        update_data = AdvertUpdatePartialDTO(
            content="New Content",
            description="New Description",
            price=30000,
            id_category=UUID(int=2)
        )

        # Act
        await service.partial_update_advert(advert_id, update_data)

        # Assert
        expected_dict = {
            "content": "New Content",
            "description": "New Description",
            "price": "30000",
            "id_category": str(UUID(int=2))
        }
        mock_repo.partial_update_advert.assert_called_once_with(advert_id, expected_dict)

    @pytest.mark.asyncio
    async def test_delete_advert_checks_existence_first(self, service, mock_repo):
        """Тест проверяет, что перед удалением проверяется существование"""
        # Arrange
        advert_id = UUID(int=1)
        user_id = UUID(int=1)
        mock_repo.get_by_id.return_value = AdvertBuilder().build()

        # Act
        await service.delete_advert(advert_id, user_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)
        mock_repo.delete_advert.assert_called_once_with(user_id, advert_id)

    @pytest.mark.asyncio
    async def test_delete_advert_raises_on_not_found(self, service, mock_repo):
        """Тест проверяет выброс исключения при отсутствии объявления"""
        # Arrange
        advert_id = UUID(int=999)
        user_id = UUID(int=1)
        mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError):
            await service.delete_advert(advert_id, user_id)

        mock_repo.delete_advert.assert_not_called()