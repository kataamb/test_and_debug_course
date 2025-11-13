# repositories/category_repository.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from abstract_repositories.icategory_repository import ICategoryRepository
from i_sql_builders.icategory_sql_builder import ICategorySqlBuilder
from models.category import Category
from uuid import UUID

class CategoryRepository(ICategoryRepository):
    def __init__(self, session: AsyncSession, builder: ICategorySqlBuilder):
        self.session = session
        self.builder = builder

    async def get_all(self) -> List[Category]:
        try:
            sql, params = self.builder.get_all()
            result = await self.session.execute(sql, params)
            print(result)
            return [Category(**row) for row in result.mappings()]
        except SQLAlchemyError as e:
            print(e)
            return []

    async def get_name_by_id(self, id_category: UUID) -> str:
        try:
            sql, params = self.builder.get_name_by_id(id_category)
            result = await self.session.execute(sql, params)
            category = result.mappings().first()
            if category:
                return category['name']
            else:
                return "Категория не найдена"
        except SQLAlchemyError:
            return "Ошибка при получении категории"