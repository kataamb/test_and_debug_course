from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from typing import AsyncGenerator
from fastapi import Request
from typing import AsyncGenerator, Literal, Union
from dataclasses import dataclass
from typing import AsyncGenerator, Literal, Union
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from clickhouse_connect.driver import AsyncClient

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine, async_sessionmaker
from sqlalchemy import text

from core.db import create_session
from core.db_config import get_db_type

# Репозитории для PostgreSQL
from repositories.advert_repository import AdvertsRepository
from repositories.category_repository import CategoryRepository
from repositories.deal_repository import DealRepository
from repositories.liked_repository import LikedRepository
from repositories.user_repository import UserRepository

# Репозитории для ClickHouse
from repositories.category_repository_ch import ClickhouseCategoryRepository
from repositories.advert_repository_ch import ClickhouseAdvertRepository
'''


from repositories.deal_repository import ClickhouseDealRepository
from repositories.liked_repository import ClickhouseLikedRepository
from repositories.user_repository import ClickhouseUserRepository
'''

# Билдеры для PostgreSQL
from sql_builders.advert_sql_builder import AdvertsSqlBuilder
from sql_builders.category_sql_builder import CategorySqlBuilder
from sql_builders.deal_sql_builder import DealSqlBuilder
from sql_builders.liked_sql_builder import LikedSqlBuilder
from sql_builders.user_sql_builder import UserSqlBuilder

# Билдеры для ClickHouse
from sql_builders.category_sql_builder_ch import ClickhouseCategorySqlBuilder
from sql_builders.advert_sql_builder_ch import ClickhouseAdvertSqlBuilder
'''


from sql_builders.clickhouse.deal_sql_builder import ClickhouseDealSqlBuilder
from sql_builders.clickhouse.liked_sql_builder import ClickhouseLikedSqlBuilder
from sql_builders.clickhouse.user_sql_builder import ClickhouseUserSqlBuilder
'''

# Сервисы
from services.advert_service import AdvertService
from services.category_service import CategoryService
from services.liked_service import LikedService
from services.deal_service import DealsService
from services.auth_service import AuthService

# -------- Data containers

@dataclass
class Repositories:
    adverts: AdvertsRepository
    categories: CategoryRepository
    deals: DealRepository
    liked: LikedRepository
    users: UserRepository

@dataclass
class Services:
    adverts: AdvertService
    categories: CategoryService
    deals: DealsService
    liked: LikedService
    auth: AuthService

@dataclass
class ServiceLocator:
    session: AsyncSession
    repositories: Repositories
    services: Services

    # Удобные геттеры
    def advert_service(self) -> AdvertService:
        return self.services.adverts

    def category_service(self) -> CategoryService:
        return self.services.categories

    def liked_service(self) -> LikedService:
        return self.services.liked

    def deals_service(self) -> DealsService:
        return self.services.deals

    def auth_service(self) -> AuthService:
        return self.services.auth

# -------- Session factory (без изменений)

async def get_async_sessionmaker(
        dsn: str | None = None,
        search_path: str = "adv_uuid",
        max_retries: int = 5,
        delay: int = 2,
) -> async_sessionmaker[AsyncSession]:
    # ... существующий код без изменений
    pass

# -------- Builder с выбором БД

async def build_service_locator(session: Union[AsyncSession, AsyncClient]) -> ServiceLocator:
    """
    Собирает билдеры, репозитории и сервисы на основе переданной сессии.
    Выбирает реализацию в зависимости от DB_TYPE.
    """
    db_type = get_db_type()


    if db_type == "clickhouse":
        print("HEREEEE")
        categories_builder = ClickhouseCategorySqlBuilder()
        categories_repo = ClickhouseCategoryRepository(session, categories_builder)

        adverts_builder = ClickhouseAdvertSqlBuilder()
        adverts_repo = ClickhouseAdvertRepository(session, adverts_builder)
        # ClickHouse билдеры
        '''
        
        
        deals_builder = ClickhouseDealSqlBuilder()
        liked_builder = ClickhouseLikedSqlBuilder()
        users_builder = ClickhouseUserSqlBuilder()

        # ClickHouse репозитории
        
        
        deals_repo = ClickhouseDealRepository(session, deals_builder)
        liked_repo = ClickhouseLikedRepository(session, liked_builder)
        users_repo = ClickhouseUserRepository(session, users_builder)
        '''
        deals_builder = DealSqlBuilder()
        liked_builder = LikedSqlBuilder()
        users_builder = UserSqlBuilder()

        # PostgreSQL репозитории
        deals_repo = DealRepository(session, deals_builder)
        liked_repo = LikedRepository(session, liked_builder)
        users_repo = UserRepository(session, users_builder)

    else:
        print(db_type)
        # PostgreSQL билдеры (по умолчанию)
        adverts_builder = AdvertsSqlBuilder()
        categories_builder = CategorySqlBuilder()
        deals_builder = DealSqlBuilder()
        liked_builder = LikedSqlBuilder()
        users_builder = UserSqlBuilder()

        # PostgreSQL репозитории
        adverts_repo = AdvertsRepository(session, adverts_builder)
        categories_repo = CategoryRepository(session, categories_builder)
        deals_repo = DealRepository(session, deals_builder)
        liked_repo = LikedRepository(session, liked_builder)
        users_repo = UserRepository(session, users_builder)

    # Сервисы (остаются без изменений, так как работают через интерфейсы)
    adverts_service = AdvertService(adverts_repo)
    categories_service = CategoryService(categories_repo)
    deals_service = DealsService(deals_repo)
    liked_service = LikedService(liked_repo)
    auth_service = AuthService(users_repo)

    return ServiceLocator(
        session=session,
        repositories=Repositories(
            adverts=adverts_repo,
            categories=categories_repo,
            deals=deals_repo,
            liked=liked_repo,
            users=users_repo,
        ),
        services=Services(
            adverts=adverts_service,
            categories=categories_service,
            deals=deals_service,
            liked=liked_service,
            auth=auth_service,
        ),
    )

# -------- FastAPI dependency (per-request) - только админ

async def get_locator(request: Request) -> AsyncGenerator[ServiceLocator, None]:
    db_type = get_db_type()

    if db_type == "clickhouse":
        print("Using ClickHouse database")
        from core.db import create_session
        client = await create_session("admin")  # await для ClickHouse
        locator = await build_service_locator(client)
        try:
            yield locator
        finally:
            await client.close()
    else:
        print("Using PostgreSQL database")
        from core.db import create_session
        # Для PostgreSQL create_session НЕ асинхронная!
        session = create_session("admin")  # БЕЗ await!
        locator = await build_service_locator(session)
        try:
            yield locator
        finally:
            await session.close()  # но close() все равно нужно await

# Упрощенная версия без поддержки разных ролей
async def get_admin_locator() -> AsyncGenerator[ServiceLocator, None]:
    """
    Альтернативная функция для получения локатора с ролью админа
    """
    session: AsyncSession = create_session("admin")
    locator = await build_service_locator(session)
    try:
        yield locator
    finally:
        await session.close()