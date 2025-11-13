from __future__ import annotations
from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from models.advert import Advert
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams


class AdvertsSqlBuilder(IAdvertSqlBuilder):
    def create(self, advert: Advert) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.adverts (content, description, id_category, price, id_seller)
            VALUES (:content, :description, :id_category, :price, :id_seller)
            RETURNING id, content, description, id_category, price, id_seller, date_created
        """)
        params: SqlParams = {
            "content": advert.content,
            "description": advert.description,
            "id_category": advert.id_category,
            "price": advert.price,
            "id_seller": advert.id_seller,
        }
        return sql, params

    def get_by_id(self, advert_id: UUID) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.adverts WHERE id = :id"), {"id": str(advert_id)}

    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.adverts ORDER BY date_created DESC"), {}

    def get_by_user(self, user_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adv_uuid.adverts WHERE id_seller = :user_id ORDER BY date_created DESC"),
            {"user_id": str(user_id)},
        )

    def is_created(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        return (
            text("SELECT 1 FROM adv_uuid.adverts WHERE id_seller = :uid AND id = :aid LIMIT 1"),
            {"uid": str(user_id), "aid": str(advert_id)},
        )

    def search_by_keyword(self, keyword_like: str) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.search_adverts(:kw)"), {"kw": keyword_like}

    def filter_by_dates(self, begin: datetime, end: datetime) -> TextAndParams:
        sql = text("""
            SELECT * FROM adv_uuid.adverts 
            WHERE date_created BETWEEN :begin_time AND :end_time
            ORDER BY date_created DESC
        """)
        return sql, {"begin_time": begin, "end_time": end}

    def by_category(self, category_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adv_uuid.adverts WHERE id_category = :category_id ORDER BY date_created DESC"),
            {"category_id": str(category_id)},
        )

    def delete(self, advert_id: UUID, user_id: UUID) -> TextAndParams:
        return (
            text("DELETE FROM adv_uuid.adverts WHERE id = :advert_id AND id_seller = :user_id"),
            {"advert_id": str(advert_id), "user_id": str(user_id)},
        )