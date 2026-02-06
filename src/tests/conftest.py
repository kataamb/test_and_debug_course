import sys
from pathlib import Path
import pytest
import tempfile
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import text
from uuid import UUID

SRC_PATH = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_PATH))

__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


@pytest.fixture
async def sqlite_db():
    """Создает временную SQLite БД для тестов"""
    # Создаем временный файл БД
    db_fd, db_path = tempfile.mkstemp(suffix='.db')
    os.close(db_fd)

    # Создаем движок для SQLite
    database_url = f"sqlite+aiosqlite:///{db_path}"
    engine = create_async_engine(database_url, echo=False)

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

    # Создаем sessionmaker
    async_session_maker = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession
    )

    yield async_session_maker, engine

    # Очистка
    await engine.dispose()
    # Удаляем временный файл
    if os.path.exists(db_path):
        os.unlink(db_path)


@pytest.fixture
async def db_session(sqlite_db):
    """Создает сессию БД для теста"""
    session_maker, engine = sqlite_db
    async with session_maker() as session:
        yield session
        await session.rollback()


@pytest.fixture
def sample_category_id():
    """Фикстура для тестового ID категории"""
    return UUID(int=1)


@pytest.fixture
def sample_user_id():
    """Фикстура для тестового ID пользователя"""
    return UUID(int=1)


@pytest.fixture
async def setup_test_data(db_session, sample_category_id, sample_user_id):
    """Создает тестовые данные в БД"""
    from tests.resources.category_test_data.mother_object_category import MotherCategory
    from tests.resources.user_test_data.mother_object_user import MotherUser

    # Создаем категорию
    category = MotherCategory.default_category()
    await db_session.execute(
        text("INSERT INTO categories (id, name) VALUES (:id, :name)"),
        {"id": str(category.id), "name": category.name}
    )

    # Создаем пользователя (профиль)
    user = MotherUser.default_user()
    await db_session.execute(
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

    # Создаем seller для пользователя (в реальной БД seller.id используется в adverts)
    seller_id = UUID(int=100)  # ID для seller (это id записи в таблице sellers)
    await db_session.execute(
        text("INSERT INTO sellers (id, profile_id, rating) VALUES (:id, :profile_id, :rating)"),
        {"id": str(seller_id), "profile_id": str(user.id), "rating": 0}
    )

    await db_session.commit()

    return {
        "category_id": category.id,
        "user_id": user.id,
        "seller_id": seller_id  # Это id записи в таблице sellers, используется в adverts.id_seller
    }
