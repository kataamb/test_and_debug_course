import os
import uuid
from typing import AsyncGenerator

import asyncpg
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from testcontainers.postgres import PostgresContainer

# ✅ НЕ ИМПОРТИРУЕМ main.py!
# Создаём своё тестовое приложение
from fastapi import FastAPI
from api_v1.routers.adverts import api_v1_adverts_router


app = FastAPI(root_path="/api/v1")
app.include_router(api_v1_adverts_router)


# ------------------------------------------------------------
# 1. Контейнер с Postgres
# ------------------------------------------------------------
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def db_url(postgres_container) -> str:
    return postgres_container.get_connection_url()


# ------------------------------------------------------------
# 2. Уникальная БД для каждого worker'а
# ------------------------------------------------------------
@pytest.fixture(scope="session")
def unique_db_name() -> str:
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    return f"test_db_{worker_id}_{uuid.uuid4().hex[:8]}"


@pytest_asyncio.fixture(scope="session")
async def test_database(db_url: str, unique_db_name: str) -> AsyncGenerator[str, None]:
    """Создаёт уникальную тестовую БД."""
    conn = await asyncpg.connect(db_url)
    try:
        await conn.execute(f"CREATE DATABASE {unique_db_name}")
        db_url_with_db = f"{db_url}/{unique_db_name}"
    finally:
        await conn.close()

    # Инициализируем схему БД
    conn = await asyncpg.connect(db_url_with_db)
    try:
        # Твои SQL-скрипты или создание таблиц напрямую
        await conn.execute("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\"")
        await conn.execute("CREATE SCHEMA IF NOT EXISTS adv_uuid")

        # Создаём таблицы (как у тебя)
        await conn.execute("""
            CREATE TABLE IF NOT EXISTS adv_uuid.categories (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                name TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.profiles (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                nickname TEXT NOT NULL,
                fio TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number TEXT,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.sellers (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                profile_id UUID NOT NULL REFERENCES adv_uuid.profiles(id) ON DELETE CASCADE,
                rating INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.customers (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                profile_id UUID NOT NULL REFERENCES adv_uuid.profiles(id) ON DELETE CASCADE,
                rating INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.adverts (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                content TEXT NOT NULL,
                description TEXT,
                id_category UUID NOT NULL REFERENCES adv_uuid.categories(id) ON DELETE CASCADE,
                price INTEGER NOT NULL,
                id_seller UUID NOT NULL REFERENCES adv_uuid.sellers(id) ON DELETE CASCADE,
                date_created TIMESTAMP DEFAULT NOW()
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.likes (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                id_customer UUID NOT NULL REFERENCES adv_uuid.customers(id) ON DELETE CASCADE,
                id_advert UUID NOT NULL REFERENCES adv_uuid.adverts(id) ON DELETE CASCADE,
                date_created TIMESTAMP DEFAULT NOW(),
                UNIQUE(id_customer, id_advert)
            );

            CREATE TABLE IF NOT EXISTS adv_uuid.deals (
                id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
                id_customer UUID NOT NULL REFERENCES adv_uuid.customers(id) ON DELETE CASCADE,
                id_advert UUID NOT NULL REFERENCES adv_uuid.adverts(id) ON DELETE CASCADE,
                date_created TIMESTAMP DEFAULT NOW(),
                address TEXT,
                UNIQUE(id_advert)
            );
        """)

        # Добавляем тестовую категорию
        await conn.execute("""
            INSERT INTO adv_uuid.categories (id, name) 
            VALUES ('bd29f255-50ab-4967-bc77-475a5fbe7952', 'Транспорт')
            ON CONFLICT (id) DO NOTHING;
        """)
    finally:
        await conn.close()

    yield db_url_with_db

    # Cleanup
    conn = await asyncpg.connect(db_url)
    try:
        await conn.execute(f"DROP DATABASE IF EXISTS {unique_db_name} WITH (FORCE)")
    finally:
        await conn.close()


# ------------------------------------------------------------
# 3. Сессия SQLAlchemy
# ------------------------------------------------------------
@pytest_asyncio.fixture
async def pg_session(test_database: str) -> AsyncGenerator[AsyncSession, None]:
    """Сессия для прямых запросов к БД."""
    async_engine_url = test_database.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_engine_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    async with async_session() as session:
        yield session

    await engine.dispose()


# ------------------------------------------------------------
# 4. HTTP-клиент для тестирования API
# ------------------------------------------------------------
@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Клиент для вызовов API."""
    async with LifespanManager(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as ac:
            yield ac


# ------------------------------------------------------------
# 5. Тестовые данные
# ------------------------------------------------------------
@pytest.fixture
def test_category_id() -> uuid.UUID:
    return uuid.UUID("bd29f255-50ab-4967-bc77-475a5fbe7952")


@pytest_asyncio.fixture
async def test_seller(pg_session: AsyncSession) -> dict:
    """Создаёт тестового продавца."""
    from uuid import uuid4

    profile_id = uuid4()
    seller_id = uuid4()

    await pg_session.execute(
        """
        INSERT INTO adv_uuid.profiles (id, nickname, fio, email, phone_number, password)
        VALUES ($1, $2, $3, $4, $5, $6)
        """,
        profile_id, "test_seller", "Test Seller", f"seller_{uuid4()}@test.com", "+1234567890", "password"
    )

    await pg_session.execute(
        """
        INSERT INTO adv_uuid.sellers (id, profile_id, rating)
        VALUES ($1, $2, $3)
        """,
        seller_id, profile_id, 0
    )

    await pg_session.commit()

    return {
        "profile_id": profile_id,
        "seller_id": seller_id,
        "email": f"seller_{profile_id}@test.com",
        "password": "password"
    }