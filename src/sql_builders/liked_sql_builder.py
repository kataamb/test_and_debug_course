from __future__ import annotations
from sqlalchemy import text
from i_sql_builders.iliked_sql_builder import ILikedSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams
from uuid import UUID

class LikedSqlBuilder(ILikedSqlBuilder):
    def add_to_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.likes (id_customer, id_advert)
            VALUES (:id_customer, :id_advert)
            RETURNING id, id_customer, id_advert, date_created
        """)
        params: SqlParams = {
            "id_customer": user_id,
            "id_advert": advert_id
        }
        return sql, params

    def remove_from_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        return (
            text("DELETE FROM adv_uuid.likes WHERE id_advert = :advert_id AND id_customer = :user_id"),
            {"advert_id": advert_id, "user_id": user_id}
        )

    def get_liked_by_user(self, user_id: UUID) -> TextAndParams:
        sql = text("""
            SELECT a.* 
            FROM adv_uuid.adverts a
            JOIN adv_uuid.likes l ON a.id = l.id_advert
            WHERE l.id_customer = :user_id
            ORDER BY a.date_created DESC
        """)
        return sql, {"user_id": user_id}

    def is_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        return (
            text("SELECT 1 FROM adv_uuid.likes WHERE id_customer = :uid AND id_advert = :aid LIMIT 1"),
            {"uid": user_id, "aid": advert_id}
        )