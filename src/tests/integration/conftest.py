# tests/integration/conftest.py
"""Конфигурация для интеграционных тестов с реальной SQLite БД"""
import sys
from pathlib import Path
import pytest
import tempfile
import os
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text

import sys
import pysqlite3

# Монки-патчим sqlite3
#sys.modules['sqlite3'] = pysqlite3

SRC_PATH = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(SRC_PATH))


@pytest.fixture(scope="function")
async def integration_db_engine():
    """Создает SQLite БД для каждого теста"""
    # Создаем временный файл БД для каждого теста
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    # ИСПОЛЬЗУЕМ aiosqlite вместо pysqlite
    database_url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(
        database_url,
        echo=False,
        connect_args={"check_same_thread": False}
    )

    # Создаем таблицы
    async with engine.begin() as conn:
        # Создаем таблицу profiles
        await conn.execute(text("""
            CREATE TABLE profiles (
                id TEXT PRIMARY KEY,
                nickname TEXT NOT NULL,
                fio TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                phone_number TEXT,
                password TEXT NOT NULL
            )
        """))

        # Создаем таблицу customers
        await conn.execute(text("""
            CREATE TABLE customers (
                id TEXT PRIMARY KEY,
                profile_id TEXT NOT NULL,
                rating INTEGER DEFAULT 0,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        """))

        # Создаем таблицу sellers
        await conn.execute(text("""
            CREATE TABLE sellers (
                id TEXT PRIMARY KEY,
                profile_id TEXT NOT NULL,
                rating INTEGER DEFAULT 0,
                FOREIGN KEY (profile_id) REFERENCES profiles(id)
            )
        """))

        # Создаем таблицу categories
        await conn.execute(text("""
            CREATE TABLE categories (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL
            )
        """))

        # Создаем таблицу adverts
        await conn.execute(text("""
            CREATE TABLE adverts (
                id TEXT PRIMARY KEY,
                content TEXT NOT NULL,
                description TEXT,
                id_category TEXT NOT NULL,
                price INTEGER NOT NULL,
                id_seller TEXT NOT NULL,
                date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (id_category) REFERENCES categories(id),
                FOREIGN KEY (id_seller) REFERENCES sellers(id)
            )
        """))

    yield engine, db_path

    # Очистка
    await engine.dispose()
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
async def integration_db_session(integration_db_engine):
    """Создает сессию БД для интеграционного теста"""
    engine, db_path = integration_db_engine
    async_session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    async with async_session_maker() as session:
        yield session
        # Очищаем все данные после теста
        try:
            await session.execute(text("DELETE FROM adverts"))
            await session.execute(text("DELETE FROM sellers"))
            await session.execute(text("DELETE FROM customers"))
            await session.execute(text("DELETE FROM profiles"))
            await session.execute(text("DELETE FROM categories"))
            await session.commit()
        except:
            await session.rollback()


@pytest.fixture
async def integration_test_data(integration_db_session):
    """Создает тестовые данные для каждого интеграционного теста"""
    from uuid import UUID
    from tests.resources.category_test_data.mother_object_category import MotherCategory
    from tests.resources.user_test_data.mother_object_user import MotherUser

    # Создаем категорию
    category = MotherCategory.default_category()
    await integration_db_session.execute(
        text("INSERT INTO categories (id, name) VALUES (:id, :name)"),
        {"id": str(category.id), "name": category.name}
    )

    # Создаем пользователя
    user = MotherUser.default_user()
    await integration_db_session.execute(
        text("""
            INSERT INTO profiles (id, nickname, fio, email, phone_number, password)
            VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
        """),
        {
            "id": str(user.id),
            "nickname": user.nickname,
            "fio": user.fio,
            "email": user.email,
            "phone_number": user.phone_number,
            "password": user.password
        }
    )

    # Создаем seller
    seller_id = UUID(int=100)
    await integration_db_session.execute(
        text("INSERT INTO sellers (id, profile_id, rating) VALUES (:id, :profile_id, :rating)"),
        {"id": str(seller_id), "profile_id": str(user.id), "rating": 0}
    )

    await integration_db_session.commit()

    return {
        "category": category,
        "user": user,
        "seller_id": seller_id
    }


@pytest.fixture
async def integration_service_locator(integration_db_session, integration_test_data):
    """Создает ServiceLocator для интеграционных тестов"""
    from service_locator import build_service_locator
    from tests.fixtures.sqlite_sql_builders import (
        SQLiteAdvertSqlBuilder,
        SQLiteCategorySqlBuilder,
        SQLiteUserSqlBuilder
    )
    from repositories.advert_repository import AdvertsRepository
    from repositories.category_repository import CategoryRepository
    from repositories.user_repository import UserRepository
    from services.advert_service import AdvertService
    from services.category_service import CategoryService
    from services.auth_service import AuthService
    from service_locator import ServiceLocator, Repositories, Services

    # Создаем репозитории с SQLite builders
    adverts_repo = AdvertsRepository(integration_db_session, SQLiteAdvertSqlBuilder())
    categories_repo = CategoryRepository(integration_db_session, SQLiteCategorySqlBuilder())
    users_repo = UserRepository(integration_db_session, SQLiteUserSqlBuilder())

    # Создаем сервисы
    adverts_service = AdvertService(adverts_repo)
    categories_service = CategoryService(categories_repo)
    auth_service = AuthService(users_repo)

    return ServiceLocator(
        session=integration_db_session,
        repositories=Repositories(
            adverts=adverts_repo,
            categories=categories_repo,
            users=users_repo,
            deals=None,
            liked=None
        ),
        services=Services(
            adverts=adverts_service,
            categories=categories_service,
            deals=None,
            liked=None,
            auth=auth_service
        )
    )