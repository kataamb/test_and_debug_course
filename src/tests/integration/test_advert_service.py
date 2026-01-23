import pytest
from unittest.mock import Mock
from testcontainers.postgres import PostgresContainer
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import text

# ==================== CONFIGURATION ====================
# Добавляем импорт pytest_asyncio
import pytest_asyncio


# ==================== UNIT TEST FIXTURES (MOCKS) ====================

@pytest.fixture
def mock_repo():
    return Mock()


@pytest.fixture
def advert_service(mock_repo):
    from services.advert_service import AdvertService
    return AdvertService(mock_repo)


# ==================== INTEGRATION TEST FIXTURES (REAL DATABASE) ====================

@pytest.fixture(scope="session")
def postgres_container():
    """Запускает PostgreSQL в Docker контейнере"""
    print("🔄 Starting PostgreSQL container for tests...")
    container = PostgresContainer("postgres:15")
    container.with_env("POSTGRES_DB", "test_db")
    container.with_env("POSTGRES_USER", "test_user")
    container.with_env("POSTGRES_PASSWORD", "test_password")
    container.start()

    print("✅ PostgreSQL container started successfully!")
    yield container
    print("🔄 Stopping PostgreSQL container...")
    container.stop()
    print("✅ PostgreSQL container stopped!")


@pytest_asyncio.fixture(scope="session")
async def async_engine(postgres_container):
    """Создает SQLAlchemy async engine"""
    # Получаем URL и меняем драйвер на asyncpg
    connection_url = postgres_container.get_connection_url().replace("psycopg2", "asyncpg")
    print(f"🔗 Connecting to database: {connection_url}")

    engine = create_async_engine(connection_url)

    # Создаем таблицы
    await create_test_tables(engine)
    print("✅ Test tables created successfully!")

    yield engine

    # Очищаем
    await engine.dispose()
    print("✅ Database engine disposed!")


@pytest_asyncio.fixture
async def db_session(async_engine) -> AsyncSession:
    """Создает тестовую сессию БД"""
    # Создаем sessionmaker и получаем сессию
    session_factory = async_sessionmaker(async_engine, expire_on_commit=False)
    session = session_factory()

    try:
        yield session
    finally:
        # Очищаем данные и закрываем сессию
        await clear_test_data(session)
        await session.close()


# ==================== TEST SERVICE FIXTURES ====================

@pytest.fixture
def test_sql_builder():
    """Минимальный тестовый SQL билдер"""

    class TestAdvertSqlBuilder:
        def create(self, advert):
            return "INSERT INTO adverts (id, content, description, price, id_category, id_seller) VALUES (:id, :content, :description, :price, :id_category, :id_seller) RETURNING *", {
                "id": advert.id,
                "content": advert.content,
                "description": advert.description,
                "price": advert.price,
                "id_category": advert.id_category,
                "id_seller": advert.id_seller
            }

        def get_by_id(self, advert_id):
            return "SELECT * FROM adverts WHERE id = :id", {"id": advert_id}

        def get_all(self):
            return "SELECT * FROM adverts", {}

    return TestAdvertSqlBuilder()


@pytest.fixture
def advert_repository(db_session, test_sql_builder):
    """Создает репозиторий с тестовым билдером"""
    from repositories.adverts_repository import AdvertsRepository
    return AdvertsRepository(db_session, test_sql_builder)


@pytest.fixture
def integration_advert_service(advert_repository):
    """Создает AdvertService с реальным репозиторием"""
    from services.advert_service import AdvertService
    return AdvertService(advert_repository)


# ==================== DATABASE HELPER FUNCTIONS ====================

async def create_test_tables(engine):
    """Создает тестовые таблицы"""
    async with engine.begin() as conn:
        await conn.execute(text("""
            DROP TABLE IF EXISTS adverts;
            CREATE TABLE adverts (
                id UUID PRIMARY KEY,
                content TEXT NOT NULL,
                description TEXT,
                price INTEGER NOT NULL,
                id_category UUID NOT NULL,
                id_seller UUID NOT NULL,
                date_created TIMESTAMP DEFAULT NOW()
            )
        """))
        await conn.commit()


async def clear_test_data(session: AsyncSession):
    """Очищает тестовые данные"""
    await session.execute(text("DELETE FROM adverts"))
    await session.commit()