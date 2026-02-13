import pytest
from httpx import AsyncClient
from uuid import UUID

pytestmark = pytest.mark.asyncio






class TestCategoriesAPI:
    """Тесты для API категорий."""

    async def test_get_all_categories(
            self,
            client: AsyncClient,
            test_database: str,  # БД уже создана и заполнена тестовыми данными
    ):
        """Тест получения списка всех категорий."""

        # 1. Вызов API
        response = await client.get("/api/v2/categories/")

        # 2. Проверка статуса
        assert response.status_code == 200

        # 3. Проверка структуры ответа
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

        # 4. Проверка количества категорий (3 штуки из test_data.sql)
        assert len(data["items"]) == 3

        # 5. Проверка наличия конкретных категорий
        category_names = [cat["name"] for cat in data["items"]]
        assert "Транспорт" in category_names
        assert "Недвижимость" in category_names
        assert "Электроника" in category_names

        # 6. Проверка структуры категории
        first_category = data["items"][0]
        assert "id" in first_category
        assert "name" in first_category
        assert isinstance(first_category["id"], str)
        assert isinstance(first_category["name"], str)
        # Проверяем, что id - валидный UUID
        assert UUID(first_category["id"])


class TestAdvertsAPI:
    """Тесты для API объявлений."""

    async def test_get_all_adverts(
            self,
            client: AsyncClient,
            test_database: str,  # БД уже создана и заполнена тестовыми данными
    ):
        """Тест получения списка всех объявлений."""

        # 1. Вызов API
        response = await client.get("/api/v2/adverts/")

        # 2. Проверка статуса
        assert response.status_code == 200

        # 3. Проверка структуры ответа
        data = response.json()
        assert "items" in data
        assert isinstance(data["items"], list)

        print(data)

        # 4. Проверка количества объявлений (2 штуки из test_data.sql)
        assert len(data["items"]) == 2

        # 5. Проверка структуры объявления
        first_advert = data["items"][0]
        assert "id" in first_advert
        assert "content" in first_advert
        assert "description" in first_advert
        assert "price" in first_advert
        assert "id_category" in first_advert
        assert "id_seller" in first_advert
        assert "date_created" in first_advert
        assert "category_name" in first_advert
        assert "seller_name" in first_advert
        assert "is_created" in first_advert
        assert "is_liked" in first_advert
        assert "is_bought" in first_advert
        assert "is_bought_by_current" in first_advert

        # 6. Проверка типов данных
        assert isinstance(first_advert["id"], str)
        assert isinstance(first_advert["content"], str)
        assert isinstance(first_advert["price"], int)
        assert isinstance(first_advert["id_category"], str)
        assert isinstance(first_advert["id_seller"], str)
        assert isinstance(first_advert["category_name"], str)
        #assert isinstance(first_advert["is_created"], bool)
        #assert isinstance(first_advert["is_liked"], bool)
        #assert isinstance(first_advert["is_bought"], bool)

        # 7. Проверка, что ID - валидные UUID
        assert UUID(first_advert["id"])
        assert UUID(first_advert["id_category"])
        assert UUID(first_advert["id_seller"])

        # 8. Проверка конкретных значений (из test_data.sql)
        assert first_advert["content"] == "Тестовое объявление 2"
        assert first_advert["price"] == 2000
        assert first_advert["id_category"] == "bd29f255-50ab-4967-bc77-475a5fbe7952"
        assert first_advert["category_name"] == "Транспорт"

        '''
        second_advert = data["items"][1]
        assert second_advert["content"] == "Тестовое объявление 1"
        assert second_advert["price"] == 2000
        assert second_advert["id_category"] == "37f7590e-aaa2-466f-8b92-113ae31507f9"
        assert second_advert["category_name"] == "Недвижимость"
        '''