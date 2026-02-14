import os
import uuid
import subprocess
from typing import AsyncGenerator


import asyncpg # type: ignore[import-untyped]
import pytest
import pytest_asyncio
from asgi_lifespan import LifespanManager
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from fastapi import FastAPI

# ============== ИМПОРТЫ ДЛЯ V2 ==============
from api_v2.routers.adverts import api_v2_router_adverts
from api_v2.routers.categories import api_v2_router_categories
from api_v2.dependencies import get_db_session

# ============================================

app = FastAPI()

# ============== ПОДКЛЮЧАЕМ V2 РОУТЕРЫ ==============
app.include_router(api_v2_router_adverts, prefix="/api/v2")
app.include_router(api_v2_router_categories, prefix="/api/v2")
# ===================================================

# ============== ПЕРЕОПРЕДЕЛЯЕМ DEPENDENCY ДЛЯ ТЕСТОВ ==============
_test_db_url = None


def set_test_db_url(url: str):
    """Устанавливаем URL тестовой БД."""
    global _test_db_url
    _test_db_url = url


async def override_get_db_session():
    """Тестовая версия get_db_session - подключается к тестовой БД."""
    global _test_db_url
    if _test_db_url is None:
        raise RuntimeError("test_db_url not set! Call set_test_db_url first.")

    # Создаем engine для тестовой БД
    async_engine_url = _test_db_url.replace("postgresql://", "postgresql+asyncpg://")
    engine = create_async_engine(async_engine_url, echo=False)
    async_session = async_sessionmaker(engine, expire_on_commit=False)

    session = async_session()
    session._test_engine = engine

    try:
        yield session
    finally:
        await session.close()
        await engine.dispose()


# ПОДМЕНЯЕМ ЗАВИСИМОСТЬ!
app.dependency_overrides[get_db_session] = override_get_db_session


# ===================================================================


@pytest.fixture(scope="session")
def db_url() -> str:
    """URL для подключения к контейнеру Postgres."""
    #return "postgresql://postgres:1234@localhost:5439/postgres"
    #if os.environ.get('CI'):
    #    return "postgresql://postgres:1234@postgres_test:5432/postgres"
    #return "postgresql://postgres:1234@localhost:5439/postgres"
    return "postgresql://postgres:1234@postgres_test:5432/postgres"


@pytest.fixture(scope="session")
def unique_db_name() -> str:
    """Уникальное имя БД для параллельных запусков."""
    worker_id = os.environ.get("PYTEST_XDIST_WORKER", "master")
    return f"test_db_{worker_id}_{uuid.uuid4().hex[:8]}"


@pytest_asyncio.fixture(scope="session")
async def test_database(db_url: str, unique_db_name: str) -> AsyncGenerator[str, None]:
    """Создаём уникальную тестовую БД."""

    # 1. Создаём БД
    conn = await asyncpg.connect(db_url)
    await conn.execute(f"CREATE DATABASE {unique_db_name}")
    await conn.close()

    db_url_with_db = f"{db_url.rsplit('/', 1)[0]}/{unique_db_name}"
    set_test_db_url(db_url_with_db)

    # 2. Создаём таблицы через psql (используем тот же URL!)
    subprocess.run([
        "psql", db_url_with_db,  # ← здесь ТОТ ЖЕ URL!
        "-f", "tests/integration/fixtures/create_tables.sql"
    ], check=True)

    # 3. Загружаем тестовые данные
    subprocess.run([
        "psql", db_url_with_db,  # ← и здесь!
        "-f", "tests/integration/fixtures/test_data.sql"
    ], check=True)

    yield db_url_with_db

    # 4. Удаляем БД
    conn = await asyncpg.connect(db_url)
    await conn.execute(f"DROP DATABASE IF EXISTS {unique_db_name} WITH (FORCE)")
    await conn.close()

@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """HTTP клиент для тестов."""
    async with LifespanManager(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test",
        ) as ac:
            yield ac
