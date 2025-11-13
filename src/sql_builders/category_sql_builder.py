from __future__ import annotations
from sqlalchemy import text
from i_sql_builders.icategory_sql_builder import ICategorySqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams
from uuid import UUID

class CategorySqlBuilder(ICategorySqlBuilder):
    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.categories"), {}

    def get_name_by_id(self, id_category: UUID) -> TextAndParams:
        return text("SELECT name FROM adv_uuid.categories WHERE id = :id"), {"id": id_category}