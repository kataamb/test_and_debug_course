# sql_builders/clickhouse/advert_sql_builder.py
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from models.advert import Advert
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams

class ClickhouseAdvertSqlBuilder(IAdvertSqlBuilder):
    def create(self, advert: Advert) -> TextAndParams:
        sql = text("""
            INSERT INTO adv.adverts 
            (id, content, description, id_category, price, id_seller, date_created)
            VALUES 
            (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
        """)
        params: SqlParams = {
            "id": int(advert.id) if advert.id else 0,
            "content": advert.content,
            "description": advert.description,
            "id_category": int(advert.id_category),
            "price": advert.price,
            "id_seller": int(advert.id_seller),
            "date_created": advert.date_created if advert.date_created else datetime.now()
        }
        return sql, params

    def get_by_id(self, advert_id: UUID) -> TextAndParams:
        return "SELECT * FROM adv_uuid.adverts WHERE id = {id:String}", {"id": str(advert_id)}

    def get_all(self) -> TextAndParams:
        return "SELECT * FROM adv_uuid.adverts ORDER BY date_created DESC", {}

    def get_by_user(self, user_id: UUID) -> TextAndParams:
        return text("SELECT * FROM adv.adverts WHERE id_seller = :user_id ORDER BY date_created DESC"), {"user_id": int(user_id)}

    def is_created(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        return text("SELECT 1 FROM adv.adverts WHERE id_seller = :uid AND id = :aid LIMIT 1"), {"uid": int(user_id), "aid": int(advert_id)}

    def search_by_keyword(self, keyword_like: str) -> TextAndParams:
        keyword = keyword_like.replace('%', '')
        return """
            SELECT * FROM adv_uuid.adverts 
            WHERE position({kw:String} in content) > 0 
            OR position({kw:String} in description) > 0
            ORDER BY date_created DESC
        """, {"kw": keyword}

    def filter_by_dates(self, begin: datetime, end: datetime) -> TextAndParams:
        return text("""
            SELECT * FROM adv.adverts 
            WHERE date_created BETWEEN :begin_time AND :end_time
            ORDER BY date_created DESC
        """), {"begin_time": begin, "end_time": end}

    def by_category(self, category_id: UUID) -> TextAndParams:
        # Возвращаем простую строку, а не text()
        return "SELECT * FROM adv_uuid.adverts WHERE id_category = {category_id:UUID} ORDER BY date_created DESC", {
            "category_id": str(category_id)
        }

    def delete(self, advert_id: UUID, user_id: UUID) -> TextAndParams:
        return text("ALTER TABLE adv.adverts DELETE WHERE id = :advert_id AND id_seller = :user_id"), {"advert_id": int(advert_id), "user_id": int(user_id)}