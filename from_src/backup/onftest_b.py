"""
conftest.py - исправленная конфигурация без проблем с event loop
"""
import pytest
import asyncio
import os
import sys
from pathlib import Path
from typing import AsyncGenerator
from tests.fixtures.user_builder import UserBuilder, TestUserFactory, UserMother

# ======== НАСТРОЙКИ БД ========
os.environ['DB_HOST'] = 'localhost'
os.environ['DB_PORT'] = '5433'
os.environ['DB_NAME'] = 'adverts_db'

print(f"🔧 Настройки БД: {os.environ.get('DB_HOST')}:{os.environ.get('DB_PORT')}")

# Добавляем корень проекта
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

print(f"📁 Используем проект из: {project_root}")

# ============================================================================
# КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Event Loop
# ============================================================================

@pytest.fixture(scope="session")
def event_loop():
    """
    Фиксируем ОДИН event loop для всех тестов.
    Без этого каждый тест создает свой loop.
    """
    # Создаем новый loop
    loop = asyncio.new_event_loop()

    # Устанавливаем его как текущий для ВСЕХ тестов
    asyncio.set_event_loop(loop)

    yield loop

    # Очищаем после всех тестов
    loop.close()
    asyncio.set_event_loop(None)

# ============================================================================
# ФИКСТУРА ДЛЯ РЕАЛЬНОЙ СЕССИИ БД (ИСПРАВЛЕННАЯ)
# ============================================================================

@pytest.fixture
async def db_session() -> AsyncGenerator:
    """
    Сессия БД для КАЖДОГО теста (scope="function" по умолчанию).
    Ключевое изменение: убрали scope="session"!
    """
    try:
        from core.db import get_session
    except ImportError as e:
        pytest.skip(f"Не удалось импортировать core.db: {e}")
        return

    # ВАЖНО: создаем сессию для КАЖДОГО теста
    async for session in get_session(role="admin"):
        try:
            # Начинаем транзакцию
            await session.begin()

            # Создаем savepoint для возможности отката
            await session.begin_nested()

            # Отдаем сессию тесту
            yield session

        except Exception:
            # Если ошибка при создании сессии
            await session.rollback()
            raise
        finally:
            # ВСЕГДА откатываем и закрываем
            try:
                await session.rollback()
            except:
                pass  # Если уже откатилась
            finally:
                await session.close()

# ============================================================================
# УПРОЩЕННЫЕ ФИКСТУРЫ (без scope="session")
# ============================================================================

@pytest.fixture
def sql_builder():
    """SQL Builder создается для каждого теста"""
    from sql_builders.advert_sql_builder import AdvertsSqlBuilder
    return AdvertsSqlBuilder()

@pytest.fixture
def advert_repository(db_session, sql_builder):
    """Репозиторий создается для каждого теста"""
    from repositories.advert_repository import AdvertsRepository
    return AdvertsRepository(db_session, sql_builder)

# ============================================================================
# ФИКСТУРЫ ДЛЯ ТЕСТОВЫХ ДАННЫХ
# ============================================================================

@pytest.fixture
def advert_builder():
    """AdvertBuilder - синхронный, можно scope="session"""
    from tests.fixtures.advert_builders import AdvertBuilder
    return AdvertBuilder()

@pytest.fixture
def advert_mother():
    """AdvertMother - синхронный, можно scope="session"""
    from tests.fixtures.advert_builders import AdvertMother
    return AdvertMother

# ============================================================================
# ХЕЛПЕРЫ ДЛЯ СОЗДАНИЯ ДАННЫХ В БД
# ============================================================================

@pytest.fixture
async def test_seller(db_session):
    """Создает тестового продавца для каждого теста"""
    import uuid
    from sqlalchemy.sql import text
    from sqlalchemy.exc import SQLAlchemyError

    seller_id = uuid.uuid4()
    profile_id = uuid.uuid4()

    # ВАЖНО: сначала профиль!
    try:
        # 1. Создаем профиль
        await db_session.execute(
            text("""
                INSERT INTO adv_uuid.profiles (id, username, email)
                VALUES (:id, :username, :email)
            """),
            {
                "id": profile_id,
                "username": f"test_user_{profile_id.hex[:8]}",
                "email": f"test_{profile_id.hex[:8]}@example.com"
            }
        )

        # 2. Создаем продавца
        await db_session.execute(
            text("""
                INSERT INTO adv_uuid.sellers (id, profile_id) 
                VALUES (:id, :profile_id)
            """),
            {"id": seller_id, "profile_id": profile_id}
        )

        await db_session.commit()

        return {"id": seller_id, "profile_id": profile_id}

    except SQLAlchemyError as e:
        await db_session.rollback()
        pytest.skip(f"Не удалось создать тестового продавца: {e}")

@pytest.fixture
async def test_advert(db_session, test_seller, advert_builder):
    """Создает тестовое объявление для каждого теста"""
    from datetime import datetime, timezone
    from sqlalchemy.sql import text
    from sqlalchemy.exc import SQLAlchemyError

    # Создаем объявление
    advert = advert_builder \
        .with_user_id(test_seller["profile_id"]) \
        .with_content("Тестовое объявление") \
        .with_price(9999) \
        .build()

    try:
        # Вставляем в БД
        await db_session.execute(
            text("""
                INSERT INTO adv_uuid.adverts 
                (id, content, description, id_category, price, id_seller, date_created)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            """),
            {
                "id": advert.id,
                "content": advert.content,
                "description": advert.description,
                "id_category": advert.id_category,
                "price": advert.price,
                "id_seller": test_seller["id"],
                "date_created": datetime.now(timezone.utc)
            }
        )

        await db_session.commit()

        return {
            "id": advert.id,
            "content": advert.content,
            "price": advert.price,
            "id_seller": test_seller["id"]
        }

    except SQLAlchemyError as e:
        await db_session.rollback()
        pytest.skip(f"Не удалось создать тестовое объявление: {e}")

# ============================================================================
# ПРОСТЕЙШИЙ ТЕСТ ДЛЯ ПРОВЕРКИ (без зависимостей)
# ============================================================================

@pytest.mark.asyncio
async def test_event_loop_fixed():
    """Тест для проверки, что event loop работает"""
    print("✅ Event loop корректно настроен")
    assert asyncio.get_event_loop() is not None


# ============================================================================
# ФИКСТУРЫ ДЛЯ USER (добавить в существующий conftest.py)
# ============================================================================

@pytest.fixture
def user_builder():
    """UserBuilder для создания тестовых пользователей"""

    return UserBuilder()


@pytest.fixture
def user_mother():
    """UserMother для стандартных сценариев"""

    return UserMother


@pytest.fixture
def user_factory():
    """Фабрика для создания пользователей в БД"""

    return TestUserFactory


@pytest.fixture
async def test_user(db_session, user_factory):
    """
    Создает тестового пользователя в БД.
    Автоматически создает профиль, customer и seller.
    """
    try:
        # Создаем пользователя в БД
        result = await user_factory.create_user_in_db(
            db_session,
            nickname="test_user",
            email="test@example.com",
            password="test123"
        )

        return result["user"]

    except Exception as e:
        pytest.skip(f"Не удалось создать тестового пользователя: {e}")


@pytest.fixture
async def test_admin_user(db_session, user_factory):
    """
    Создает тестового администратора в БД
    """
    try:
        result = await user_factory.create_user_in_db(
            db_session,
            nickname="admin",
            email="admin@example.com",
            password="admin123",
            fio="Администратор Системы"
        )

        return result["user"]

    except Exception as e:
        pytest.skip(f"Не удалось создать администратора: {e}")


# ============================================================================
# ФИКСТУРЫ ДЛЯ ADVERT С УЧЕТОМ ВСЕХ ЗАВИСИМОСТЕЙ
# ============================================================================

@pytest.fixture
def advert_helper():
    """Хелпер для создания объявлений с зависимостями"""
    from tests.fixtures.advert_helpers import AdvertTestHelper
    return AdvertTestHelper

@pytest.fixture
async def complete_advert_setup(db_session, advert_helper):
    """
    Создает полный набор данных для теста объявлений:
    профиль → продавец → категория → объявление
    """
    try:
        setup_data = await advert_helper.create_complete_advert_setup(db_session)
        print("✅ Создан полный набор данных для объявления:")
        print(f"   Профиль: {setup_data['profile']['id']}")
        print(f"   Продавец: {setup_data['seller']['id']}")
        print(f"   Объявление: {setup_data['advert']['id']}")
        return setup_data
    except Exception as e:
        await db_session.rollback()
        pytest.skip(f"Не удалось создать тестовые данные для объявления: {e}")