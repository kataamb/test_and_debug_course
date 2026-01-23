# i_sql_builders/deal_sql_builder.py
from __future__ import annotations
from sqlalchemy import text
from i_sql_builders.ideal_sql_builder import IDealSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams
from uuid import UUID

class DealSqlBuilder(IDealSqlBuilder):
    def create_deal(self, user_id: UUID, advert_id: UUID, address: str = "online") -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.deals (id_customer, id_advert, address)
            SELECT c.id, :advert_id, :address
            FROM adv_uuid.customers c
            WHERE c.profile_id = :user_id
            RETURNING id, id_customer, id_advert, date_created, address
        """)
        params: SqlParams = {
            "user_id": user_id,
            "advert_id": advert_id,
            "address": address
        }
        return sql, params

    def get_deals_by_user(self, user_id: UUID) -> TextAndParams:
        sql = text("""
            SELECT a.* 
            FROM adv_uuid.adverts a
            JOIN adv_uuid.deals d ON a.id = d.id_advert
            JOIN adv_uuid.customers c ON d.id_customer = c.id
            WHERE c.profile_id = :user_id
            ORDER BY a.date_created DESC
        """)
        return sql, {"user_id": user_id}

    def is_in_deals(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        sql = text("""
            SELECT 1 
            FROM adv_uuid.deals d
            JOIN adv_uuid.customers c ON d.id_customer = c.id
            WHERE c.profile_id = :uid AND d.id_advert = :aid 
            LIMIT 1
        """)
        return sql, {"uid": user_id, "aid": advert_id}

    def is_bought(self, advert_id: UUID) -> TextAndParams:
        return (
            text("SELECT 1 FROM adv_uuid.deals WHERE id_advert = :aid LIMIT 1"),
            {"aid": advert_id}
        )