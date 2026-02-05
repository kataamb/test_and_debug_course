#import factory and mother of adverts

from unittest.mock import Mock
import pytest
from services.advert_service import AdvertService

# tests/unit/service/advert_service_classic_test.py
import pytest
import asyncio
from uuid import UUID
from unittest.mock import AsyncMock, MagicMock
from services.advert_service import AdvertService
from models.advert import Advert
from api_v1.dto.advert_dto import AdvertUpdatePartialDTO
from tests.resources.advert_test_data.builder_advert import AdvertBuilder
from tests.resources.advert_test_data.mother_object_advert import MotherAdvert
from tests.resources.user_test_data.mother_object_user import MotherUser


class TestAdvertServiceClassic:
    """Классические тесты для AdvertService (без моков на репозиторий)"""

    @pytest.fixture
    def mock_repo(self):
        """Фикстура для создания mock репозитория"""
        return AsyncMock()

    @pytest.fixture
    def service(self, mock_repo):
        """Фикстура для создания сервиса с mock репозиторием"""
        return AdvertService(mock_repo)

    @pytest.fixture
    def sample_advert(self):
        """Фикстура для тестового объявления"""
        return AdvertBuilder().build()

    @pytest.mark.asyncio
    async def test_create_advert_success(self, service, mock_repo, sample_advert):
        """Позитивный тест создания объявления"""
        # Arrange
        expected_advert = sample_advert
        mock_repo.create.return_value = expected_advert

        # Act
        result = await service.create_advert(sample_advert)

        # Assert
        mock_repo.create.assert_called_once_with(sample_advert)
        assert result == expected_advert

    @pytest.mark.asyncio
    async def test_create_advert_failure(self, service, mock_repo, sample_advert):
        """Негативный тест создания объявления (репозиторий возвращает None)"""
        # Arrange
        mock_repo.create.return_value = None

        # Act
        result = await service.create_advert(sample_advert)

        # Assert
        mock_repo.create.assert_called_once_with(sample_advert)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_advert_success(self, service, mock_repo):
        """Позитивный тест получения объявления по ID"""
        # Arrange
        advert_id = UUID(int=1)
        expected_advert = AdvertBuilder().with_id(1).build()
        mock_repo.get_by_id.return_value = expected_advert

        # Act
        result = await service.get_advert(advert_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)
        assert result == expected_advert

    @pytest.mark.asyncio
    async def test_get_advert_not_found(self, service, mock_repo):
        """Негативный тест получения несуществующего объявления"""
        # Arrange
        advert_id = UUID(int=999)
        mock_repo.get_by_id.return_value = None

        # Act
        result = await service.get_advert(advert_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)
        assert result is None

    @pytest.mark.asyncio
    async def test_get_all_adverts(self, service, mock_repo):
        """Позитивный тест получения всех объявлений"""
        # Arrange
        expected_adverts = [
            AdvertBuilder().with_id(1).build(),
            AdvertBuilder().with_id(2).build()
        ]
        mock_repo.get_all_adverts.return_value = expected_adverts

        # Act
        result = await service.get_all_adverts()

        # Assert
        mock_repo.get_all_adverts.assert_called_once()
        assert result == expected_adverts
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_get_advert_by_user(self, service, mock_repo):
        """Позитивный тест получения объявлений пользователя"""
        # Arrange
        user_id = MotherUser.default_user().id
        expected_adverts = [
            AdvertBuilder().with_id(1).with_seller(user_id).build(),
            AdvertBuilder().with_id(2).with_seller(user_id).build()
        ]
        mock_repo.get_advert_by_user.return_value = expected_adverts

        # Act
        result = await service.get_advert_by_user(user_id)

        # Assert
        mock_repo.get_advert_by_user.assert_called_once_with(user_id)
        assert result == expected_adverts

    @pytest.mark.asyncio
    async def test_is_created_true(self, service, mock_repo):
        """Позитивный тест проверки создания объявления пользователем"""
        # Arrange
        user_id = UUID(int=1)
        advert_id = UUID(int=1)
        mock_repo.is_created.return_value = True

        # Act
        result = await service.is_created(user_id, advert_id)

        # Assert
        mock_repo.is_created.assert_called_once_with(user_id, advert_id)
        assert result is True

    @pytest.mark.asyncio
    async def test_is_created_false(self, service, mock_repo):
        """Негативный тест проверки создания объявления пользователем"""
        # Arrange
        user_id = UUID(int=1)
        advert_id = UUID(int=1)
        mock_repo.is_created.return_value = False

        # Act
        result = await service.is_created(user_id, advert_id)

        # Assert
        mock_repo.is_created.assert_called_once_with(user_id, advert_id)
        assert result is False

    @pytest.mark.asyncio
    async def test_get_adverts_by_key_word(self, service, mock_repo):
        """Позитивный тест поиска по ключевому слову"""
        # Arrange
        keyword = "smartphone"
        expected_adverts = [AdvertBuilder().with_content("smartphone").build()]
        mock_repo.get_adverts_by_key_word.return_value = expected_adverts

        # Act
        result = await service.get_adverts_by_key_word(keyword)

        # Assert
        mock_repo.get_adverts_by_key_word.assert_called_once_with(keyword)
        assert result == expected_adverts

    @pytest.mark.asyncio
    async def test_get_adverts_by_category(self, service, mock_repo):
        """Позитивный тест поиска по категории"""
        # Arrange
        category_id = UUID(int=1)
        expected_adverts = [AdvertBuilder().with_category_id(category_id).build()]
        mock_repo.get_adverts_by_category.return_value = expected_adverts

        # Act
        result = await service.get_adverts_by_category(category_id)

        # Assert
        mock_repo.get_adverts_by_category.assert_called_once_with(category_id)
        assert result == expected_adverts

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_both(self, service, mock_repo):
        """Позитивный тест поиска по категории и ключевому слову (оба параметра)"""
        # Arrange
        keyword = "smartphone"
        category_id = UUID(int=1)
        expected_adverts = [AdvertBuilder().build()]
        mock_repo.get_adverts_by_category_and_keyword.return_value = expected_adverts

        # Act
        result = await service.get_adverts_by_category_and_keyword(keyword, category_id)

        # Assert
        mock_repo.get_adverts_by_category_and_keyword.assert_called_once_with(keyword, category_id)
        assert result == expected_adverts

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_only_keyword(self, service, mock_repo):
        """Тест поиска только по ключевому слову"""
        # Arrange
        keyword = "smartphone"
        category_id = None
        expected_adverts = [AdvertBuilder().build()]
        mock_repo.get_adverts_by_key_word.return_value = expected_adverts

        # Act
        result = await service.get_adverts_by_category_and_keyword(keyword, category_id)

        # Assert
        mock_repo.get_adverts_by_key_word.assert_called_once_with(keyword)
        assert result == expected_adverts

    @pytest.mark.asyncio
    async def test_update_advert_success(self, service, mock_repo):
        """Позитивный тест полного обновления"""
        # Arrange
        advert_id = UUID(int=1)
        advert_data = AdvertBuilder().with_content("Updated").build()
        expected_result = advert_data
        mock_repo.update_advert.return_value = expected_result

        # Act
        result = await service.update_advert(advert_id, advert_data)

        # Assert
        mock_repo.update_advert.assert_called_once_with(advert_id, advert_data)
        assert result == expected_result

    @pytest.mark.asyncio
    async def test_partial_update_advert_success(self, service, mock_repo):
        """Позитивный тест частичного обновления"""
        # Arrange
        advert_id = UUID(int=1)
        update_data = AdvertUpdatePartialDTO(
            content="Updated Content",
            price=25000
        )
        expected_advert = AdvertBuilder().with_content("Updated Content").with_price(25000).build()
        mock_repo.partial_update_advert.return_value = expected_advert

        # Act
        result = await service.partial_update_advert(advert_id, update_data)

        # Assert
        expected_dict = {
            "content": "Updated Content",
            "price": "25000"
        }
        mock_repo.partial_update_advert.assert_called_once_with(advert_id, expected_dict)
        assert result == expected_advert

    @pytest.mark.asyncio
    async def test_delete_advert_success(self, service, mock_repo):
        """Позитивный тест удаления объявления"""
        # Arrange
        advert_id = UUID(int=1)
        user_id = UUID(int=1)
        advert = AdvertBuilder().with_id(1).build()
        mock_repo.get_by_id.return_value = advert
        mock_repo.delete_advert.return_value = None

        # Act
        await service.delete_advert(advert_id, user_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)
        mock_repo.delete_advert.assert_called_once_with(user_id, advert_id)

    @pytest.mark.asyncio
    async def test_delete_advert_not_found(self, service, mock_repo):
        """Негативный тест удаления несуществующего объявления"""
        # Arrange
        advert_id = UUID(int=999)
        user_id = UUID(int=1)
        mock_repo.get_by_id.return_value = None

        # Act & Assert
        with pytest.raises(ValueError, match="Advert not found"):
            await service.delete_advert(advert_id, user_id)

        mock_repo.get_by_id.assert_called_once_with(advert_id)
        mock_repo.delete_advert.assert_not_called()