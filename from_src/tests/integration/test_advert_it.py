import pytest
from httpx import AsyncClient
from uuid import UUID, uuid4  # ← добавил uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from services.auth_service import AuthService
from repositories.user_repository import UserRepository
from sql_builders.user_sql_builder import UserSqlBuilder

from sqlalchemy import text

@pytest.mark.asyncio
class TestAdvertsAPI:
    """Интеграционные тесты для API объявлений (v1)."""

    # --------------------------------------------------------
    # Тест 1: Успешное создание объявления
    # --------------------------------------------------------
    async def test_create_advert_success(
            self,
            client: AsyncClient,
            pg_session: AsyncSession,
            test_category_id: UUID
    ):
        # 1. Создаём продавца
        user_repo = UserRepository(pg_session, UserSqlBuilder())
        auth_service = AuthService(user_repo)

        test_user = User(
            nickname="testuser",
            fio="Test User",
            email=f"user_{uuid4()}@test.com",  # ← ИСПРАВЛЕНО
            phone_number="+1234567890",
            password="password123"
        )
        created_user = await auth_service.register(test_user)

        # 2. Получаем seller_id
        result = await pg_session.execute(
            "SELECT id FROM adv_uuid.sellers WHERE profile_id = $1",
            created_user.id
        )
        seller_row = result.first()
        assert seller_row is not None
        seller_id = seller_row[0]

        # 3. Данные для объявления
        advert_data = {
            "content": "Integration Test Advert",
            "description": "Created during API test",
            "price": 999,
            "id_category": str(test_category_id)
        }

        # 4. Вызов API
        response = await client.post(
            "/api/v1/adverts/",
            json=advert_data,
            headers={"X-Test-User-Id": str(created_user.id)}
        )

        # 5. Проверки
        assert response.status_code == 201
        data = response.json()
        assert data["content"] == "Integration Test Advert"
        assert data["price"] == 999
        assert UUID(data["id"]) is not None
        assert data["id_seller"] == str(seller_id)

    # --------------------------------------------------------
    # Тест 2: Попытка создать объявление без авторизации
    # --------------------------------------------------------
    async def test_create_advert_unauthorized(
            self,
            client: AsyncClient,
            test_category_id: UUID
    ):
        advert_data = {
            "content": "Should Fail",
            "description": "No auth",
            "price": 500,
            "id_category": str(test_category_id)
        }

        response = await client.post("/api/v1/adverts/", json=advert_data)
        assert response.status_code == 403  # Теперь будет работать

    # --------------------------------------------------------
    # Тест 3: Получение списка объявлений
    # --------------------------------------------------------
    async def test_get_all_adverts(
            self,
            client: AsyncClient,
            pg_session: AsyncSession,
            test_category_id: UUID,
            test_seller: dict
    ):
        seller_id = test_seller["seller_id"]

        # ✅ ПРОСТОЙ И ЧИСТЫЙ SQL
        await pg_session.execute(
            text("""
                INSERT INTO adv_uuid.adverts 
                    (id, content, description, id_category, price, id_seller, date_created) 
                VALUES 
                    (gen_random_uuid(), 'Test Advert 1', 'Description 1', :cat_id, 100, :seller_id, now()),
                    (gen_random_uuid(), 'Test Advert 2', 'Description 2', :cat_id, 200, :seller_id, now())
            """),
            {
                "cat_id": test_category_id,
                "seller_id": seller_id
            }
        )
        await pg_session.commit()

        response = await client.get("/api/v1/adverts/")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 2

    async def test_get_all_adverts(
            self,
            client: AsyncClient,
            pg_session: AsyncSession,
            test_category_id: UUID,
            test_seller: dict
    ):
        seller_id = test_seller["seller_id"]

        # ⚠️ ИСПРАВЛЕНО: используем :param и словарь
        await pg_session.execute(
            text("""
                    INSERT INTO adv_uuid.adverts (id, content, description, id_category, price, id_seller, date_created)
                    VALUES 
                    (gen_random_uuid(), 'Test Advert 1', 'Description 1', :cat_id, :price1, :seller_id, NOW()),
                    (gen_random_uuid(), 'Test Advert 2', 'Description 2', :cat_id, :price2, :seller_id, NOW())
                """),
            {
                "cat_id": test_category_id,
                "seller_id": seller_id,
                "price1": 100,
                "price2": 200
            }
        )
        await pg_session.commit()

        # 2. Вызов API
        response = await client.get("/api/v1/adverts/")

        # 3. Проверки
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert len(data["items"]) >= 2

        first_advert = data["items"][0]
        assert "content" in first_advert
        assert "price" in first_advert
        assert "id_category" in first_advert


async def test_get_all_adverts2(
        self,
        client: AsyncClient,
        test_category_id: UUID,
        test_seller: dict  # ← это фикстура уже создаёт продавца в БД
):
    # 1. Создаём объявление через API (не лезем в БД!)
    advert_data = {
        "content": "Test Advert 1",
        "description": "Description 1",
        "price": 100,
        "id_category": str(test_category_id)
    }

    response = await client.post(
        "/api/v1/adverts/",
        json=advert_data,
        headers={"X-Test-User-Id": str(test_seller["profile_id"])}
    )
    assert response.status_code == 201

    # 2. Создаём второе объявление
    advert_data["content"] = "Test Advert 2"
    advert_data["price"] = 200
    response = await client.post(
        "/api/v1/adverts/",
        json=advert_data,
        headers={"X-Test-User-Id": str(test_seller["profile_id"])}
    )
    assert response.status_code == 201

    # 3. Получаем список объявлений
    response = await client.get("/api/v1/adverts/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert len(data["items"]) >= 2