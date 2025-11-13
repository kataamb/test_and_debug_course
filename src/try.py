import asyncio
from uuid import uuid4
from core.db import SessionLocal
from models.user import User
from sql_builders.user_sql_builder import  UserSqlBuilder
from repositories.user_repository import UserRepository

async def create_user():
    # Создаем уникальные данные
    unique_id = uuid4()
    unique_email = f"test_{unique_id}@example.com"
    unique_nickname = f"testuser_{unique_id}"

    user = User(
        id=unique_id,
        nickname=unique_nickname,
        fio="Тест Тестович",
        email=unique_email,
        phone_number="+1234567890",
        password="password123"
    )

    async with SessionLocal["admin"]() as session:
        try:
            builder = UserSqlBuilder()
            repo = UserRepository(session, builder)

            created = await repo.create(user)
            print(f"Пользователь создан: {created}")

        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")


    asyncio.run(create_user())