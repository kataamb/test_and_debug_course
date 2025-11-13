import pytest_asyncio
import pytest
from models.user import User
from repositories.user_repository import UserRepository
from sql_builders.user_sql_builder import UserSqlBuilder
from core.db import SessionLocal
from uuid import UUID, uuid4
from sqlalchemy.exc import IntegrityError


@pytest_asyncio.fixture
async def admin_session():
    async with SessionLocal["admin"]() as session:
        try:
            yield session
        finally:
            await session.close()




