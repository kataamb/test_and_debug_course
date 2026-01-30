from __future__ import annotations

from dataclasses import dataclass
from typing import AsyncGenerator
from fastapi import Request
from typing import Union
from sqlalchemy.ext.asyncio import AsyncSession
from clickhouse_connect.driver import AsyncClient

from sqlalchemy.ext.asyncio import async_sessionmaker

from core.db import create_session
from core.db_config import get_db_type

# Репозитории для PostgreSQL
from repositories.advert_repository import AdvertsRepository
from repositories.category_repository import CategoryRepository
from repositories.deal_repository import DealRepository
from repositories.liked_repository import LikedRepository
from repositories.user_repository import UserRepository


# Билдеры для PostgreSQL
from sql_builders.advert_sql_builder import AdvertsSqlBuilder
from sql_builders.category_sql_builder import CategorySqlBuilder
from sql_builders.deal_sql_builder import DealSqlBuilder
from sql_builders.liked_sql_builder import LikedSqlBuilder
from sql_builders.user_sql_builder import UserSqlBuilder


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
    get_db_type()

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