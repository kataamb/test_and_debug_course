import json
import os
from pathlib import Path
from typing import Literal, Union, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from clickhouse_connect import get_async_client
from clickhouse_connect.driver import AsyncClient

# Определяем тип сессии (может быть AsyncSession или AsyncClient)
SessionType = Union[AsyncSession, AsyncClient]

def get_db_type() -> str:
    """Определяет тип БД из переменных окружения"""
    return os.getenv("DB_TYPE", "postgres").lower()

# Загружаем конфиг
config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

db_cfg = config["database"]

db_type = get_db_type()

if db_type == "clickhouse":
    # CLICKHOUSE CONFIGURATION
    CLICKHOUSE_HOST = os.getenv("CLICKHOUSE_HOST", "localhost")
    CLICKHOUSE_PORT = int(os.getenv("CLICKHOUSE_PORT", 8123))
    CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "default")
    CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "default")
    CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "")

    # Клиент ClickHouse
    async def create_clickhouse_client() -> AsyncClient:
        return await get_async_client(
            host=CLICKHOUSE_HOST,
            port=CLICKHOUSE_PORT,
            username=CLICKHOUSE_USER,
            password=CLICKHOUSE_PASSWORD,
            database=CLICKHOUSE_DB,
        )

    # Для совместимости с существующим кодом
    SessionLocal = {
        "admin": create_clickhouse_client,
        "authorized_user": create_clickhouse_client,
        "any_user": create_clickhouse_client,
    }

    async def create_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncClient:
        return await create_clickhouse_client()

    async def get_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncGenerator[AsyncClient, None]:
        client = await create_clickhouse_client()
        try:
            yield client
        finally:
            await client.close()

else:
    # POSTGRESQL CONFIGURATION
    host = os.getenv("DB_HOST", db_cfg["host"])
    port = int(os.getenv("DB_PORT", db_cfg["port"]))
    db_name = os.getenv("DB_NAME", db_cfg["name"])

    DATABASES = {
        role: f"postgresql+asyncpg://{creds['username']}:{creds['password']}@{host}:{port}/{db_name}"
        for role, creds in db_cfg["users"].items()
    }

    _engines = {role: create_async_engine(url, future=True) for role, url in DATABASES.items()}

    async_sessionmakers = {
        role: async_sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
        for role, engine in _engines.items()
    }

    SessionLocal = async_sessionmakers

    # ДЛЯ POSTGRESQL ФУНКЦИЯ НЕ АСИНХРОННАЯ!
    def create_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncSession:
        return async_sessionmakers[role]()

    # НО get_session ДОЛЖНА БЫТЬ АСИНХРОННОЙ!
    async def get_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncGenerator[AsyncSession, None]:
        async_session = async_sessionmakers[role]()
        try:
            yield async_session
        finally:
            await async_session.close()

# Простая утилита для проверки типа сессии
def is_clickhouse(session: SessionType) -> bool:
    """Проверяет, является ли сессия ClickHouse клиентом"""
    return hasattr(session, 'query') and not hasattr(session, 'execute')