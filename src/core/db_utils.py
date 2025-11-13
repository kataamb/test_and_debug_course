# core/db_utils.py
from typing import Union, Any
from sqlalchemy.ext.asyncio import AsyncSession
from clickhouse_connect.driver import AsyncClient

async def execute_query(session: Union[AsyncSession, AsyncClient], query: Any, params: dict = None) -> Any:
    """Универсальная функция выполнения запроса для обеих БД"""
    if hasattr(session, 'query'):  # ClickHouse
        return await session.query(str(query), parameters=params)
    else:  # PostgreSQL
        if params:
            return await session.execute(query, params)
        else:
            return await session.execute(query)

def is_clickhouse(session: Union[AsyncSession, AsyncClient]) -> bool:
    """Проверяет, является ли сессия ClickHouse клиентом"""
    return hasattr(session, 'query') and not hasattr(session, 'execute')