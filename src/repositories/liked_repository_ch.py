# repositories/liked_repository.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from abstract_repositories.iliked_repository import ILikedRepository
from i_sql_builders.iliked_sql_builder import ILikedSqlBuilder
from models.advert import Advert
from models.liked import Liked
from uuid import UUID

class LikedRepository(ILikedRepository):
    def __init__(self, session: AsyncSession, builder: ILikedSqlBuilder):
        self.session = session
        self.builder = builder

    async def add_to_liked(self, user_id: UUID, advert_id: UUID) -> Optional[Liked]:
        try:
            sql, params = self.builder.add_to_liked(user_id, advert_id)
            result = await self.session.execute(sql, params)
            print("AAAA", result)
            row = result.mappings().first()
            await self.session.commit()
            return Liked(**row) if row else None
        except SQLAlchemyError as e:
            print('error', e)
            await self.session.rollback()
            return None

    async def remove_from_liked(self, user_id: UUID, advert_id: UUID) -> None:
        try:
            sql, params = self.builder.remove_from_liked(user_id, advert_id)
            await self.session.execute(sql, params)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()

    async def get_liked_by_user(self, user_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.get_liked_by_user(user_id)
            result = await self.session.execute(sql, params)
            return [Advert(**row) for row in result.mappings()]
        except SQLAlchemyError:
            return []

    async def is_liked(self, user_id: UUID, advert_id: UUID) -> bool:
        try:
            sql, params = self.builder.is_liked(user_id, advert_id)
            result = await self.session.execute(sql, params)
            return result.first() is not None
        except SQLAlchemyError:
            return False