from sqlalchemy import text
from models.history_deal import HistoryDeal
from i_sql_builders.ihistory_deal_sql_builder import IHistoryDealSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams
from uuid import UUID

class HistoryDealSqlBuilder(IHistoryDealSqlBuilder):
    def create(self, history_deal: HistoryDeal) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.history_deals (id_deal, id_customer, status)
            VALUES (:id_deal, :id_customer, :status)
            RETURNING id, id_deal, id_customer, status, date_created
        """)
        params: SqlParams = {
            "id_deal": history_deal.id_deal,
            "id_customer": history_deal.id_customer,
            "status": history_deal.status,
        }
        return sql, params

    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.history_deals ORDER BY date_created DESC"), {}

    def get_by_user(self, user_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adv_uuid.history_deals WHERE id_customer = :uid ORDER BY date_created DESC"),
            {"uid": str(user_id)}
        )
