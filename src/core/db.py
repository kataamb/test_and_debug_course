import json
import os
from pathlib import Path
from typing import Literal, AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

def get_db_type() -> str:
    """Определяет тип БД из переменных окружения"""
    return os.getenv("DB_TYPE", "postgres").lower()

# Загружаем конфиг
config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

db_cfg = config["database"]

# Всегда используем PostgreSQL
host = os.getenv("DB_HOST", db_cfg["host"])
port = int(os.getenv("DB_PORT", db_cfg["port"]))
db_name = os.getenv("DB_NAME", db_cfg["name"])

# Создаем DSN для разных ролей
DATABASES = {
    role: f"postgresql+asyncpg://{creds['username']}:{creds['password']}@{host}:{port}/{db_name}"
    for role, creds in db_cfg["users"].items()
}

# Создаем движки
_engines = {
    role: create_async_engine(url, future=True, echo=False)
    for role, url in DATABASES.items()
}

# Создаем фабрики сессий
async_sessionmakers = {
    role: async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
        autoflush=False
    )
    for role, engine in _engines.items()
}

# Для совместимости с существующим кодом
SessionLocal = async_sessionmakers

def create_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncSession:
    """
    Создает новую сессию PostgreSQL.
    Внимание: эта функция НЕ асинхронная!
    """
    return async_sessionmakers[role]()

async def get_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный генератор сессий для использования в FastAPI dependencies.
    Пример: async with get_session() as session:
    """
    async_session = async_sessionmakers[role]()
    try:
        yield async_session
    finally:
        await async_session.close()

def is_clickhouse(session) -> bool:
    """
    Проверяет, является ли сессия ClickHouse клиентом.
    Для PostgreSQL всегда возвращает False.
    """
    return False