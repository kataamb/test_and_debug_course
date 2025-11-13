from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from models.history_deal import HistoryDeal
from models.advert import Advert
from abstract_repositories.ihistory_deal_repository import IHistoryDealRepository
from i_sql_builders.ihistory_deal_sql_builder import IHistoryDealSqlBuilder

class HistoryDealRepository(IHistoryDealRepository):
    def __init__(self, session: AsyncSession, builder: IHistoryDealSqlBuilder):
        self.session = session
        self.builder = builder

    async def create(self, history_deal: HistoryDeal) -> HistoryDeal:
        try:
            sql, params = self.builder.create(history_deal)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            await self.session.commit()
            return HistoryDeal(**row)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all(self) -> List[HistoryDeal]:
        sql, params = self.builder.get_all()
        result = await self.session.execute(sql, params)
        return [HistoryDeal(**row) for row in result.mappings()]

    async def get_by_user(self, user_id):
        sql, params = self.builder.get_by_user(user_id)
        result = await self.session.execute(sql, params)
        return [HistoryDeal(**row) for row in result.mappings()]
