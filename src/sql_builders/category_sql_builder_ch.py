# sql_builders/clickhouse/category_sql_builder.py
from __future__ import annotations
from sqlalchemy import text
from i_sql_builders.icategory_sql_builder import ICategorySqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams
from uuid import UUID

class ClickhouseCategorySqlBuilder(ICategorySqlBuilder):
    def get_all(self) -> TextAndParams:
        return "SELECT * FROM adv_uuid.categories", {}  # ← Простая строка!

    def get_name_by_id(self, id_category: UUID) -> TextAndParams:
        return "SELECT name FROM adv_uuid.categories WHERE id = {id:String}", {"id": str(id_category)}