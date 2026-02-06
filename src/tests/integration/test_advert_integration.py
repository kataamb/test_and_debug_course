# tests/integration/test_advert_integration.py
"""Интеграционные тесты для AdvertService с реальной SQLite БД"""
import pytest

from datetime import datetime, timezone
from service_locator import ServiceLocator
from tests.resources.advert_test_data.builder_advert import AdvertBuilder
from tests.resources.category_test_data.mother_object_category import MotherCategory
from tests.resources.user_test_data.mother_object_user import MotherUser
from sqlalchemy import text


class TestAdvertServiceIntegration:
    """Интеграционные тесты для AdvertService с реальной SQLite"""

    @pytest.mark.asyncio
    async def test_create_advert_integration(self, integration_service_locator, integration_test_data):
        """Интеграционный тест создания объявления"""
        # Arrange
        advert_service = integration_service_locator.services.adverts
        advert = AdvertBuilder().with_id(1).with_category_id(
            integration_test_data["category"].id
        ).with_seller(integration_test_data["seller_id"]).build()

        # Act
        result = await advert_service.create_advert(advert)

        # Assert
        assert result is not None
        assert result.id == advert.id
        assert result.content == advert.content

        # Проверяем через сервис
        retrieved = await advert_service.get_advert(advert.id)
        assert retrieved is not None
        assert retrieved.content == advert.content

    @pytest.mark.asyncio
    async def test_get_all_adverts_integration(self, integration_service_locator, integration_test_data,
                                               integration_db_session):
        """Интеграционный тест получения всех объявлений"""
        # Arrange
        advert_service = integration_service_locator.services.adverts
        adverts = [
            AdvertBuilder().with_id(1).with_category_id(
                integration_test_data["category"].id
            ).with_seller(integration_test_data["seller_id"]).build(),
            AdvertBuilder().with_id(2).with_category_id(
                integration_test_data["category"].id
            ).with_seller(integration_test_data["seller_id"]).build()
        ]

        for advert in adverts:
            await advert_service.create_advert(advert)

        # Act
        result = await advert_service.get_all_adverts()

        # Assert
        assert len(result) == 2
        assert any(a.id == adverts[0].id for a in result)
        assert any(a.id == adverts[1].id for a in result)

    @pytest.mark.asyncio
    async def test_update_advert_integration(self, integration_service_locator, integration_test_data):
        """Интеграционный тест обновления объявления"""
        # Arrange
        advert_service = integration_service_locator.services.adverts
        advert = AdvertBuilder().with_id(1).with_category_id(
            integration_test_data["category"].id
        ).with_seller(integration_test_data["seller_id"]).build()

        created = await advert_service.create_advert(advert)

        # Обновляем
        updated_advert = AdvertBuilder().with_id(1).with_content("Updated Content").build()
        updated_advert.id_category = integration_test_data["category"].id
        updated_advert.id_seller = integration_test_data["seller_id"]

        # Act
        result = await advert_service.update_advert(created.id, updated_advert)

        # Assert
        assert result.content == "Updated Content"

        # Проверяем через get
        retrieved = await advert_service.get_advert(created.id)
        assert retrieved.content == "Updated Content"

    @pytest.mark.asyncio
    async def test_delete_advert_integration(self, integration_service_locator, integration_test_data):
        """Интеграционный тест удаления объявления"""
        # Arrange
        advert_service = integration_service_locator.services.adverts
        advert = AdvertBuilder().with_id(1).with_category_id(
            integration_test_data["category"].id
        ).with_seller(integration_test_data["seller_id"]).build()

        created = await advert_service.create_advert(advert)

        # Act
        await advert_service.delete_advert(created.id, integration_test_data["user"].id)

        # Assert
        retrieved = await advert_service.get_advert(created.id)
        assert retrieved is None

    @pytest.mark.asyncio
    async def test_search_by_keyword_integration(self, integration_service_locator, integration_test_data):
        """Интеграционный тест поиска по ключевому слову"""
        # Arrange
        advert_service = integration_service_locator.services.adverts
        advert = AdvertBuilder().with_id(1).with_content("smartphone").with_category_id(
            integration_test_data["category"].id
        ).with_seller(integration_test_data["seller_id"]).build()

        await advert_service.create_advert(advert)

        # Act
        result = await advert_service.get_adverts_by_key_word("smartphone")

        # Assert
        assert len(result) == 1
        assert "smartphone" in result[0].content.lower()

        # Тест на случайность
        result = await advert_service.get_adverts_by_key_word("laptop")
        assert len(result) == 0