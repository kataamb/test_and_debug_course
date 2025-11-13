import json
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import Literal

# Загружаем конфиг
config_path = Path(__file__).parent.parent / "config.json"
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

db_cfg = config["database"]

# Можно переопределить из переменных окружения при docker-compose up
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

def create_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user") -> AsyncSession:
    return async_sessionmakers[role]()

async def get_session(role: Literal["admin", "authorized_user", "any_user"] = "any_user"):
    async_session = async_sessionmakers[role]()
    try:
        return async_session
    finally:
        await async_session.close()
