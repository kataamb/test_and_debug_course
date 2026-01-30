import pytest_asyncio
from core.db import SessionLocal


@pytest_asyncio.fixture
async def admin_session():
    async with SessionLocal["admin"]() as session:
        try:
            yield session
        finally:
            await session.close()




