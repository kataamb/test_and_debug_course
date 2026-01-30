from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from abstract_repositories.iadvert_repository import IAdvertRepository
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from models.advert import Advert
from datetime import datetime

class AdvertsRepository(IAdvertRepository):
    def __init__(self, session: AsyncSession, builder: IAdvertSqlBuilder):
        self.session = session
        self.builder = builder

    async def create(self, advert: Advert) -> Advert:
        try:
            sql, params = self.builder.create(advert)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            print(row)
            await self.session.commit()

            if row is None:
                raise ValueError("Failed to create advert - no data returned")
            return Advert(**row)
        except IntegrityError:
            await self.session.rollback()
            raise
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_by_id(self, advert_id: UUID) -> Advert:
        try:
            sql, params = self.builder.get_by_id(advert_id)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            if not row:
                raise ValueError(f"Advert with id {advert_id} not found")
            return Advert(**row)
        except SQLAlchemyError:
            raise

    async def get_all_adverts(self) -> List[Advert]:
        try:
            sql, params = self.builder.get_all()
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def get_advert_by_user(self, user_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.get_by_user(user_id)
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def is_created(self, user_id: UUID, advert_id: UUID) -> bool:
        try:
            sql, params = self.builder.is_created(user_id, advert_id)
            result = await self.session.execute(sql, params)
            return result.first() is not None
        except SQLAlchemyError:
            return False

    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]:
        try:
            sql, params = self.builder.search_by_keyword(f"%{key_word}%")
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def get_adverts_by_filter(self, begin_time: datetime, end_time: datetime) -> List[Advert]:
        try:
            sql, params = self.builder.filter_by_dates(begin_time, end_time)
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.by_category(category_id)
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def get_adverts_by_category_and_keyword(self, keyword: str, category_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.by_category_and_keyword(keyword, category_id)
            result = await self.session.execute(sql, params)
            return [Advert(**r) for r in result.mappings()]
        except SQLAlchemyError:
            raise

    async def update_advert(self, advert_id: UUID, advert: Advert) -> Advert:
        """
        Полное обновление объявления
        """
        try:
            sql, params = self.builder.update_full(advert_id, advert)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            if not row:
                raise ValueError(f"Advert with id {advert_id} not found")
            await self.session.commit()
            return Advert(**row)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def partial_update_advert(self, advert_id: UUID, update_data: dict) -> Advert:
        """
        Частичное обновление объявления
        """
        try:
            sql, params = self.builder.update_partial(advert_id, update_data)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            if not row:
                raise ValueError(f"Advert with id {advert_id} not found")
            await self.session.commit()
            return Advert(**row)
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None:
        try:
            sql, params = self.builder.delete(advert_id, user_id)
            await self.session.execute(sql, params)
            await self.session.commit()
        except SQLAlchemyError:
            await self.session.rollback()
            raise