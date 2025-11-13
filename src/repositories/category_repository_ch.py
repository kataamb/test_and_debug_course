# repositories/category_repository.py (для ClickHouse версии)
from core.db_utils import execute_query
from models.category import *
from typing import List
from clickhouse_connect.driver import AsyncClient
from clickhouse_connect.driver.exceptions import ClickHouseError
from abstract_repositories.icategory_repository import ICategoryRepository
from i_sql_builders.icategory_sql_builder import ICategorySqlBuilder
from models.category import Category
from uuid import UUID
import logging


class ClickhouseCategoryRepository(ICategoryRepository):
    def __init__(self, client: AsyncClient, builder: ICategorySqlBuilder):
        self.client = client
        self.builder = builder

    async def get_all(self) -> List[Category]:
        try:
            sql, params = self.builder.get_all()
            # Используем универсальную функцию
            result = await execute_query(self.client, sql, params)

            if hasattr(result, 'result_set'):  # ClickHouse
                if not result.result_rows:
                    return []
                categories = []
                for row in result.result_set:
                    category = Category(id=row[0], name=row[1])
                    categories.append(category)
                return categories
            else:  # PostgreSQL
                return [Category(**row) for row in result.mappings()]

        except Exception as e:
            return []

    async def get_name_by_id(self, id_category: UUID) -> str:
        try:
            sql, params = self.builder.get_name_by_id(id_category)
            # Для ClickHouse используем query()
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return "Категория не найдена"

            # ClickHouse возвращает результат в result_set
            return result.result_set[0][0]  # Первая колонка первого ряда

        except Exception as e:
            return "Ошибка при получении категории"