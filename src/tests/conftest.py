'''
import pytest
import psycopg2
import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()


@pytest.fixture(scope="function")
def db_connection():
    """
    Фикстура для подключения к БД.
    Scope=function означает, что фикстура будет выполняться для каждой тестовой функции.
    """
    connection = None
    try:
        # Получаем параметры подключения из переменных окружения
        db_params = {
            'host': 'localhost',
            'port': '5433',
            'database': 'adverts_db',
            'user': 'postgres',
            'password': '1234'
        }

        # Убираем None значения, если какие-то параметры не заданы
        db_params = {k: v for k, v in db_params.items() if v is not None}

        # Подключаемся к БД
        print(f"Подключаюсь к БД с параметрами: {db_params}")
        connection = psycopg2.connect(**db_params)

        # Возвращаем соединение тесту
        yield connection

    except Exception as e:
        pytest.fail(f"Не удалось подключиться к БД: {e}")

    finally:
        # Закрываем соединение после выполнения теста
        if connection:
            connection.close()
            print("Соединение с БД закрыто")


'''

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
import asyncio


@pytest.fixture(scope="session")
def event_loop():
    """Event loop для асинхронных тестов"""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def async_session(event_loop):
    """Фикстура создает реальный AsyncSession для тестов"""
    # Создаем engine с asyncpg драйвером
    engine = create_async_engine(
        "postgresql+asyncpg://postgres:1234@localhost:5433/adverts_db",
        echo=True  # видим SQL запросы в консоли
    )

    # Создаем фабрику сессий
    async_session_factory = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # Создаем сессию
    async with async_session_factory() as session:
        yield session

    # Закрываем engine после теста
    await engine.dispose()