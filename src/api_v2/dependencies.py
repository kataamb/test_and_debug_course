"""Все зависимости в одном месте для легкой подмены в тестах."""
from __future__ import annotations

from typing import AsyncGenerator, Optional
from uuid import UUID

from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.db import create_session as create_prod_session
from service_locator import build_service_locator, ServiceLocator


# ============== 1. Сессия БД (легко подменяется) ==============
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Единственное место, где создается сессия БД.
    В тестах мы просто подменим эту функцию!
    """
    # По умолчанию - продакшен сессия
    session = create_prod_session("admin")
    try:
        yield session
    finally:
        await session.close()


# ============== 2. Service Locator ==============
async def get_service_locator(
        session: AsyncSession = Depends(get_db_session)
) -> AsyncGenerator[ServiceLocator, None]:
    """Создает ServiceLocator с переданной сессией."""
    locator = await build_service_locator(session)
    yield locator


# ============== 3. Текущий пользователь ==============
async def get_current_user(
        request: Request,
        locator: ServiceLocator = Depends(get_service_locator)
) -> Optional[dict]:
    """JWT авторизация."""
    token = request.cookies.get("access_token")
    if not token:
        return None

    from core.create_jwt import JWTManager
    try:
        payload = JWTManager.decode_token(token)
        return {
            "id": UUID(payload.get("id")),
            "email": payload.get("sub"),
            "role": payload.get("role"),
        }
    except Exception:
        return None


# ============== 4. Опциональный пользователь ==============
async def get_optional_user(
        current_user: Optional[dict] = Depends(get_current_user)
) -> Optional[dict]:
    """Для эндпоинтов, где авторизация необязательна."""
    return current_user