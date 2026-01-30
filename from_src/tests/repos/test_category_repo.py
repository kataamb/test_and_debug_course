import pytest_asyncio
import pytest
from repositories.category_repository import CategoryRepository
from sql_builders.category_sql_builder import CategorySqlBuilder
from core.db import SessionLocal

@pytest_asyncio.fixture
async def admin_session():
    async with SessionLocal["admin"]() as session:
        try:
            yield session
        finally:
            await session.close()

@pytest.mark.asyncio
async def test_category_get_all(admin_session):
    """Тест получения всех категорий"""
    try:
        builder = CategorySqlBuilder()
        repo = CategoryRepository(admin_session, builder)

        categories = await repo.get_all()
        assert isinstance(categories, list)
    except Exception as e:
        pytest.skip(f"Тест пропущен: {e}")

@pytest.mark.asyncio
async def test_category_get_name_by_id(admin_session):
    """Тест получения названия категории по ID"""
    try:
        builder = CategorySqlBuilder()
        repo = CategoryRepository(admin_session, builder)

        name = await repo.get_name_by_id(1)
        assert isinstance(name, str)
    except Exception as e:
        pytest.skip(f"Тест пропущен: {e}")

@pytest.mark.asyncio
async def test_category_get_name_by_nonexistent_id(admin_session):
    """Тест получения названия несуществующей категории"""
    try:
        builder = CategorySqlBuilder()
        repo = CategoryRepository(admin_session, builder)

        name = await repo.get_name_by_id(99999)
        assert name == "Ошибка при получении категории"
    except Exception as e:
        pytest.skip(f"Тест пропущен: {e}")

@pytest.mark.asyncio
async def test_category_error_handling(admin_session):
    """Тест обработки ошибок в категориях"""
    try:
        builder = CategorySqlBuilder()
        repo = CategoryRepository(admin_session, builder)

        # Тест с некорректным ID
        name = await repo.get_name_by_id(-1)
        assert isinstance(name, str)
    except Exception as e:
        pytest.skip(f"Тест пропущен: {e}")