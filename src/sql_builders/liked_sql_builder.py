# i_sql_builders/liked_sql_builder.py
from __future__ import annotations
from sqlalchemy import text
from i_sql_builders.iliked_sql_builder import ILikedSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams
from uuid import UUID

class LikedSqlBuilder(ILikedSqlBuilder):
    def add_to_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.likes (id_customer, id_advert)
            SELECT c.id, :advert_id
            FROM adv_uuid.customers c
            WHERE c.profile_id = :user_id
            RETURNING id, id_customer, id_advert, date_created
        """)
        params: SqlParams = {
            "user_id": user_id,
            "advert_id": advert_id
        }
        return sql, params

    def remove_from_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        sql = text("""
            DELETE FROM adv_uuid.likes l
            USING adv_uuid.customers c
            WHERE l.id_advert = :advert_id 
            AND l.id_customer = c.id 
            AND c.profile_id = :user_id
        """)
        return sql, {"advert_id": advert_id, "user_id": user_id}

    def get_liked_by_user(self, user_id: UUID) -> TextAndParams:
        sql = text("""
            SELECT a.* 
            FROM adv_uuid.adverts a
            JOIN adv_uuid.likes l ON a.id = l.id_advert
            JOIN adv_uuid.customers c ON l.id_customer = c.id
            WHERE c.profile_id = :user_id
            ORDER BY a.date_created DESC
        """)
        return sql, {"user_id": user_id}

    def is_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        sql = text("""
            SELECT 1 
            FROM adv_uuid.likes l
            JOIN adv_uuid.customers c ON l.id_customer = c.id
            WHERE c.profile_id = :uid AND l.id_advert = :aid 
            LIMIT 1
        """)
        return sql, {"uid": user_id, "aid": advert_id}# i_sql_builders/liked_sql_builder.py
