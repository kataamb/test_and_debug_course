# repositories/deal_repository.py
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from abstract_repositories.ideal_repository import IDealRepository
from i_sql_builders.ideal_sql_builder import IDealSqlBuilder
from models.advert import Advert
from models.deal import Deal
from uuid import UUID

class DealRepository(IDealRepository):
    def __init__(self, session: AsyncSession, builder: IDealSqlBuilder):
        self.session = session
        self.builder = builder

    async def create_deal(self, user_id: UUID, advert_id: UUID) -> Deal:
        try:
            sql, params = self.builder.create_deal(user_id, advert_id)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            await self.session.commit()
            if row is None:
                raise SQLAlchemyError("INSERT INTO adv.deals returned no row")
            return Deal(**row)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def get_deals_by_user(self, user_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.get_deals_by_user(user_id)
            result = await self.session.execute(sql, params)
            return [Advert(**row) for row in result.mappings()]
        except SQLAlchemyError:
            return []

    async def is_in_deals(self, user_id: UUID, advert_id: UUID) -> bool:
        try:
            sql, params = self.builder.is_in_deals(user_id, advert_id)
            result = await self.session.execute(sql, params)
            return result.first() is not None
        except SQLAlchemyError:
            return False

    async def is_bought(self, advert_id: UUID) -> bool:
        try:
            sql, params = self.builder.is_bought(advert_id)
            result = await self.session.execute(sql, params)
            return result.first() is not None
        except SQLAlchemyError:
            return False