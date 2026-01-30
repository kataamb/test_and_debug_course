# repositories/advert_repository_ch.py
from typing import List, Optional
from uuid import UUID
from clickhouse_connect.driver import AsyncClient
from clickhouse_connect.driver.exceptions import ClickHouseError
from abstract_repositories.iadvert_repository import IAdvertRepository
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from models.advert import Advert
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ClickhouseAdvertRepository(IAdvertRepository):
    def __init__(self, client: AsyncClient, builder: IAdvertSqlBuilder):
        self.client = client
        self.builder = builder

    async def create(self, advert: Advert) -> Optional[Advert]:
        try:
            sql, params = self.builder.create(advert)
            await self.client.command(sql, parameters=params)

            if advert.id:
                return await self.get_by_id(advert.id)
            return advert

        except ClickHouseError as e:
            logger.error(f"Error creating advert: {e}")
            return None

    async def get_by_id(self, advert_id: UUID) -> Optional[Advert]:
        try:
            sql, params = self.builder.get_by_id(advert_id)
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return None

            row = result.result_set[0]
            column_names = result.column_names

            # Создаем словарь из результата
            row_dict = dict(zip(column_names, row))
            return Advert(**row_dict)

        except ClickHouseError as e:
            logger.error(f"Error getting advert by id: {e}")
            return None

    async def get_all_adverts(self) -> List[Advert]:
        try:
            sql, params = self.builder.get_all()
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return []

            column_names = result.column_names
            adverts = []

            for row in result.result_set:
                row_dict = dict(zip(column_names, row))
                adverts.append(Advert(**row_dict))

            return adverts

        except ClickHouseError as e:
            logger.error(f"Error getting all adverts: {e}")
            return []

    async def get_advert_by_user(self, user_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.get_by_user(user_id)
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return []

            column_names = result.column_names
            adverts = []

            for row in result.result_set:
                row_dict = dict(zip(column_names, row))
                adverts.append(Advert(**row_dict))

            return adverts

        except ClickHouseError as e:
            logger.error(f"Error getting user adverts: {e}")
            return []

    async def is_created(self, user_id: UUID, advert_id: UUID) -> bool:
        try:
            sql, params = self.builder.is_created(user_id, advert_id)
            result = await self.client.query(sql, parameters=params)
            return bool(result and result.result_rows)

        except ClickHouseError as e:
            logger.error(f"Error checking if advert exists: {e}")
            return False

    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]:
        try:
            sql, params = self.builder.search_by_keyword(key_word)
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return []

            column_names = result.column_names
            adverts = []

            for row in result.result_set:
                row_dict = dict(zip(column_names, row))
                adverts.append(Advert(**row_dict))

            return adverts

        except ClickHouseError as e:
            logger.error(f"Error searching adverts: {e}")
            return []

    async def get_adverts_by_filter(self, begin_time: datetime, end_time: datetime) -> List[Advert]:
        try:
            sql, params = self.builder.filter_by_dates(begin_time, end_time)
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return []

            column_names = result.column_names
            adverts = []

            for row in result.result_set:
                row_dict = dict(zip(column_names, row))
                adverts.append(Advert(**row_dict))

            return adverts

        except ClickHouseError as e:
            logger.error(f"Error filtering adverts by date: {e}")
            return []

    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]:
        try:
            sql, params = self.builder.by_category(category_id)
            result = await self.client.query(sql, parameters=params)

            if not result or not result.result_rows:
                return []

            column_names = result.column_names
            adverts = []

            for row in result.result_set:
                row_dict = dict(zip(column_names, row))
                adverts.append(Advert(**row_dict))

            return adverts

        except ClickHouseError as e:
            logger.error(f"Error getting adverts by category: {e}")
            return []

    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None:
        try:
            sql, params = self.builder.delete(advert_id, user_id)
            await self.client.command(sql, parameters=params)

        except ClickHouseError as e:
            logger.error(f"Error deleting advert: {e}")
            raise