import pytest
import uuid
from unittest.mock import AsyncMock, Mock
from services.advert_service import AdvertService
from tests.fixtures.advert_builders import AdvertBuilder, AdvertUpdateBuilder, AdvertMother


class TestAdvertServiceMocked:
    """Unit-тесты для AdvertService с моками (Лондонский стиль)"""

    @pytest.fixture
    def mock_repo(self):
        return Mock()

    @pytest.fixture
    def service(self, mock_repo):
        return AdvertService(mock_repo)

    # POSITIVE TESTS
    @pytest.mark.asyncio
    async def test_create_advert_success(self, service, mock_repo):
        """Позитивный тест создания объявления"""
        # Arrange
        advert = AdvertMother.create_valid_advert()
        mock_repo.create = AsyncMock(return_value=advert)

        # Act
        result = await service.create_advert(advert)

        # Assert
        assert result == advert
        mock_repo.create.assert_called_once_with(advert)

    @pytest.mark.asyncio
    async def test_get_advert_success(self, service, mock_repo):
        """Позитивный тест получения объявления"""
        # Arrange
        advert_id = uuid.uuid4()
        expected_advert = AdvertMother.create_valid_advert()
        mock_repo.get_by_id = AsyncMock(return_value=expected_advert)

        # Act
        result = await service.get_advert(advert_id)

        # Assert
        assert result == expected_advert
        mock_repo.get_by_id.assert_called_once_with(advert_id)

    @pytest.mark.asyncio
    async def test_get_all_adverts_success(self, service, mock_repo):
        """Позитивный тест получения всех объявлений"""
        # Arrange
        adverts = [AdvertMother.create_valid_advert(), AdvertMother.create_valid_advert()]
        mock_repo.get_all_adverts = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_all_adverts()

        # Assert
        assert result == adverts
        assert len(result) == 2
        mock_repo.get_all_adverts.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_advert_by_user_success(self, service, mock_repo):
        """Позитивный тест получения объявлений пользователя"""
        # Arrange
        user_id = uuid.uuid4()
        user_adverts = [AdvertMother.create_advert_with_user(user_id)]
        mock_repo.get_advert_by_user = AsyncMock(return_value=user_adverts)

        # Act
        result = await service.get_advert_by_user(user_id)

        # Assert
        assert result == user_adverts
        assert len(result) == 1
        mock_repo.get_advert_by_user.assert_called_once_with(user_id)

    @pytest.mark.asyncio
    async def test_is_created_true(self, service, mock_repo):
        """Позитивный тест проверки создания"""
        # Arrange
        user_id = uuid.uuid4()
        advert_id = uuid.uuid4()
        mock_repo.is_created = AsyncMock(return_value=True)

        # Act
        result = await service.is_created(user_id, advert_id)

        # Assert
        assert result is True
        mock_repo.is_created.assert_called_once_with(user_id, advert_id)

    @pytest.mark.asyncio
    async def test_get_adverts_by_key_word_success(self, service, mock_repo):
        """Позитивный тест поиска по ключевому слову"""
        # Arrange
        keyword = "test"
        adverts = [AdvertBuilder().with_title("Test Advert").build()]
        mock_repo.get_adverts_by_key_word = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_key_word(keyword)

        # Assert
        assert result == adverts
        mock_repo.get_adverts_by_key_word.assert_called_once_with(keyword)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_success(self, service, mock_repo):
        """Позитивный тест получения объявлений по категории"""
        # Arrange
        category_id = uuid.uuid4()
        adverts = [AdvertBuilder().build()]
        mock_repo.get_adverts_by_category = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_category(category_id)

        # Assert
        assert result == adverts
        mock_repo.get_adverts_by_category.assert_called_once_with(category_id)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_both_provided(self, service, mock_repo):
        """Позитивный тест поиска по категории и ключевому слову (оба параметра)"""
        # Arrange
        keyword = "test"
        category_id = uuid.uuid4()
        adverts = [AdvertBuilder().with_title("Test Advert").build()]
        mock_repo.get_adverts_by_category_and_keyword = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_category_and_keyword(keyword, category_id)

        # Assert
        assert result == adverts
        mock_repo.get_adverts_by_category_and_keyword.assert_called_once_with(keyword, category_id)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_only_keyword(self, service, mock_repo):
        """Позитивный тест поиска только по ключевому слову"""
        # Arrange
        keyword = "test"
        adverts = [AdvertBuilder().with_title("Test Advert").build()]
        mock_repo.get_adverts_by_key_word = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_category_and_keyword(keyword, None)

        # Assert
        assert result == adverts
        mock_repo.get_adverts_by_key_word.assert_called_once_with(keyword)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_only_category(self, service, mock_repo):
        """Позитивный тест поиска только по категории"""
        # Arrange
        category_id = uuid.uuid4()
        adverts = [AdvertBuilder().build()]
        mock_repo.get_adverts_by_category = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_category_and_keyword(None, category_id)

        # Assert
        assert result == adverts
        mock_repo.get_adverts_by_category.assert_called_once_with(category_id)

    @pytest.mark.asyncio
    async def test_get_adverts_by_category_and_keyword_no_params(self, service, mock_repo):
        """Позитивный тест поиска без параметров (все объявления)"""
        # Arrange
        adverts = [AdvertBuilder().build(), AdvertBuilder().build()]
        mock_repo.get_all_adverts = AsyncMock(return_value=adverts)

        # Act
        result = await service.get_adverts_by_category_and_keyword(None, None)

        # Assert
        assert result == adverts
        mock_repo.get_all_adverts.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_advert_success(self, service, mock_repo):
        """Позитивный тест полного обновления объявления"""
        # Arrange
        advert_id = uuid.uuid4()
        advert_data = AdvertMother.create_valid_advert()
        updated_advert = AdvertBuilder().with_title("Updated Title").build()
        mock_repo.update_advert = AsyncMock(return_value=updated_advert)

        # Act
        result = await service.update_advert(advert_id, advert_data)

        # Assert
        assert result == updated_advert
        mock_repo.update_advert.assert_called_once_with(advert_id, advert_data)

    @pytest.mark.asyncio
    async def test_partial_update_advert_success(self, service, mock_repo):
        """Позитивный тест частичного обновления объявления"""
        # Arrange
        advert_id = uuid.uuid4()
        update_data = AdvertUpdateBuilder().with_title("New Title").with_price(500.0).build()
        updated_advert = AdvertBuilder().with_title("New Title").with_price(500.0).build()
        mock_repo.partial_update_advert = AsyncMock(return_value=updated_advert)

        # Act
        result = await service.partial_update_advert(advert_id, update_data)

        # Assert
        assert result == updated_advert
        mock_repo.partial_update_advert.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_advert_success(self, service, mock_repo):
        """Позитивный тест удаления объявления"""
        # Arrange
        advert_id = uuid.uuid4()
        user_id = uuid.uuid4()
        existing_advert = AdvertMother.create_advert_with_user(user_id)
        mock_repo.get_by_id = AsyncMock(return_value=existing_advert)
        mock_repo.delete_advert = AsyncMock()

        # Act
        await service.delete_advert(advert_id, user_id)

        # Assert
        mock_repo.get_by_id.assert_called_once_with(advert_id)
        mock_repo.delete_advert.assert_called_once_with(user_id, advert_id)

    # NEGATIVE TESTS
    @pytest.mark.asyncio
    async def test_get_advert_not_found(self, service, mock_repo):
        """Негативный тест - объявление не найдено"""
        # Arrange
        advert_id = uuid.uuid4()
        mock_repo.get_by_id = AsyncMock(return_value=None)

        # Act
        result = await service.get_advert(advert_id)

        # Assert
        assert result is None
        mock_repo.get_by_id.assert_called_once_with(advert_id)

    @pytest.mark.asyncio
    async def test_is_created_false(self, service, mock_repo):
        """Негативный тест - объявление не создано пользователем"""
        # Arrange
        user_id = uuid.uuid4()
        advert_id = uuid.uuid4()
        mock_repo.is_created = AsyncMock(return_value=False)

        # Act
        result = await service.is_created(user_id, advert_id)

        # Assert
        assert result is False
        mock_repo.is_created.assert_called_once_with(user_id, advert_id)

    @pytest.mark.asyncio
    async def test_delete_advert_not_found_raises_exception(self, service, mock_repo):
        """Негативный тест - исключение при удалении несуществующего объявления"""
        # Arrange
        advert_id = uuid.uuid4()
        user_id = uuid.uuid4()
        mock_repo.get_by_id = AsyncMock(return_value=None)

        # Act & Assert
        with pytest.raises(ValueError, match="Advert not found"):
            await service.delete_advert(advert_id, user_id)

        mock_repo.get_by_id.assert_called_once_with(advert_id)
        mock_repo.delete_advert.assert_not_called()

    # BUILDER PATTERN TESTS
    @pytest.mark.asyncio
    async def test_create_advert_with_builder(self, service, mock_repo):
        """Тест с использованием Data Builder pattern"""
        # Arrange
        advert = AdvertBuilder().with_title("Special Offer").with_price(999).build()
        mock_repo.create = AsyncMock(return_value=advert)

        # Act
        result = await service.create_advert(advert)

        # Assert
        assert result == advert
        assert result.content == "Special Offer"
        assert result.price == 999
        mock_repo.create.assert_called_once_with(advert)

    @pytest.mark.asyncio
    async def test_partial_update_with_builder(self, service, mock_repo):
        """Тест частичного обновления с использованием Builder"""
        # Arrange
        advert_id = uuid.uuid4()
        update_data = AdvertUpdateBuilder().with_title("Updated").with_description("New desc").build()
        updated_advert = AdvertBuilder().with_title("Updated").build()
        mock_repo.partial_update_advert = AsyncMock(return_value=updated_advert)

        # Act
        result = await service.partial_update_advert(advert_id, update_data)

        # Assert
        assert result == updated_advert
        mock_repo.partial_update_advert.assert_called_once()

    # OBJECT MOTHER PATTERN TESTS
    @pytest.mark.asyncio
    async def test_create_advert_with_object_mother(self, service, mock_repo):
        """Тест с использованием Object Mother pattern"""
        # Arrange
        advert = AdvertMother.create_expensive_advert()
        mock_repo.create = AsyncMock(return_value=advert)

        # Act
        result = await service.create_advert(advert)

        # Assert
        assert result == advert
        assert result.price == 10000.0
        mock_repo.create.assert_called_once_with(advert)