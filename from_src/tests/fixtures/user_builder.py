"""
User Builders and Mother Object
Для создания тестовых пользователей и профилей
"""
import uuid
from faker import Faker
from typing import Optional, Dict, Any

fake = Faker()


class UserBuilder:
    """Data Builder для создания объектов User"""

    def __init__(self):
        self.user_data = {
            "id": uuid.uuid4(),
            "nickname": fake.user_name(),
            "fio": fake.name(),
            "email": fake.email(),
            "phone_number": fake.phone_number(),
            "password": fake.password(length=12),
            "rating": fake.random_int(min=0, max=5)
        }

    def with_id(self, user_id: uuid.UUID) -> 'UserBuilder':
        self.user_data["id"] = user_id
        return self

    def with_nickname(self, nickname: str) -> 'UserBuilder':
        self.user_data["nickname"] = nickname
        return self

    def with_fio(self, fio: str) -> 'UserBuilder':
        """ФИО пользователя"""
        self.user_data["fio"] = fio
        return self

    def with_email(self, email: str) -> 'UserBuilder':
        self.user_data["email"] = email
        return self

    def with_phone_number(self, phone_number: str) -> 'UserBuilder':
        self.user_data["phone_number"] = phone_number
        return self

    def with_password(self, password: str) -> 'UserBuilder':
        self.user_data["password"] = password
        return self

    def with_rating(self, rating: int) -> 'UserBuilder':
        """Рейтинг для customer/seller"""
        self.user_data["rating"] = rating
        return self

    def build(self):
        """Создает объект User для использования в приложении"""
        from models.user import User
        return User(
            id=self.user_data["id"],
            nickname=self.user_data["nickname"],
            fio=self.user_data["fio"],
            email=self.user_data["email"],
            phone_number=self.user_data["phone_number"],
            password=self.user_data["password"]
        )

    def build_profile_data(self) -> Dict[str, Any]:
        """Возвращает данные для вставки в таблицу profiles"""
        return {
            "id": self.user_data["id"],
            "nickname": self.user_data["nickname"],
            "fio": self.user_data["fio"],
            "email": self.user_data["email"],
            "phone_number": self.user_data["phone_number"],
            "password": self.user_data["password"]
        }

    def build_customer_data(self) -> Dict[str, Any]:
        """Возвращает данные для вставки в таблицу customers"""
        return {
            "profile_id": self.user_data["id"],
            "rating": self.user_data["rating"]
        }

    def build_seller_data(self) -> Dict[str, Any]:
        """Возвращает данные для вставки в таблицу sellers"""
        return {
            "profile_id": self.user_data["id"],
            "rating": self.user_data["rating"]
        }


class UserMother:
    """Object Mother pattern для стандартных пользователей"""

    @staticmethod
    def create_valid_user():
        """Создает валидного пользователя"""
        return UserBuilder().build()

    @staticmethod
    def create_user_with_email(email: str):
        """Создает пользователя с конкретным email"""
        return UserBuilder().with_email(email).build()

    @staticmethod
    def create_user_with_nickname(nickname: str):
        """Создает пользователя с конкретным никнеймом"""
        return UserBuilder().with_nickname(nickname).build()

    @staticmethod
    def create_admin_user():
        """Создает пользователя-администратора"""
        return UserBuilder() \
            .with_nickname("admin") \
            .with_fio("Администратор Системы") \
            .with_email("admin@example.com") \
            .with_password("admin123") \
            .build()

    @staticmethod
    def create_test_user():
        """Создает стандартного тестового пользователя"""
        return UserBuilder() \
            .with_nickname("test_user") \
            .with_fio("Тестовый Пользователь") \
            .with_email("test@example.com") \
            .with_password("test123") \
            .build()

    @staticmethod
    def create_high_rating_user():
        """Создает пользователя с высоким рейтингом"""
        return UserBuilder().with_rating(5).build()

    @staticmethod
    def create_low_rating_user():
        """Создает пользователя с низким рейтингом"""
        return UserBuilder().with_rating(1).build()

    @staticmethod
    def create_user_with_phone(phone_number: str):
        """Создает пользователя с конкретным номером телефона"""
        return UserBuilder().with_phone_number(phone_number).build()


class TestUserFactory:
    """Фабрика для создания тестовых пользователей в БД"""

    @staticmethod
    async def create_user_in_db(session, user_builder: Optional[UserBuilder] = None, **kwargs):
        """
        Создает пользователя в БД (профиль + customer + seller)
        Возвращает созданного пользователя и данные для cleanup
        """
        from sqlalchemy.sql import text

        # Создаем builder или используем переданный
        if user_builder is None:
            user_builder = UserBuilder()

        # Применяем дополнительные параметры
        for key, value in kwargs.items():
            if hasattr(user_builder, f"with_{key}"):
                getattr(user_builder, f"with_{key}")(value)

        # Получаем данные
        profile_data = user_builder.build_profile_data()
        customer_data = user_builder.build_customer_data()
        seller_data = user_builder.build_seller_data()
        user = user_builder.build()

        try:
            # 1. Создаем профиль
            await session.execute(
                text("""
                    INSERT INTO adv_uuid.profiles 
                    (id, nickname, fio, email, phone_number, password)
                    VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
                """),
                profile_data
            )

            # 2. Создаем customer
            await session.execute(
                text("""
                    INSERT INTO adv_uuid.customers (profile_id, rating)
                    VALUES (:profile_id, :rating)
                """),
                customer_data
            )

            # 3. Создаем seller
            await session.execute(
                text("""
                    INSERT INTO adv_uuid.sellers (profile_id, rating)
                    VALUES (:profile_id, :rating)
                """),
                seller_data
            )

            await session.commit()

            print(f"✅ Создан пользователь в БД: {user.email} (ID: {user.id})")

            return {
                "user": user,
                "profile_data": profile_data,
                "customer_data": customer_data,
                "seller_data": seller_data
            }

        except Exception as e:
            await session.rollback()
            raise Exception(f"Не удалось создать пользователя в БД: {e}")

    @staticmethod
    async def delete_user_from_db(session, profile_id: uuid.UUID):
        """Удаляет пользователя из БД"""
        from sqlalchemy.sql import text

        try:
            # Удаляем в правильном порядке (из-за внешних ключей)
            await session.execute(
                text("DELETE FROM adv_uuid.customers WHERE profile_id = :id"),
                {"id": profile_id}
            )

            await session.execute(
                text("DELETE FROM adv_uuid.sellers WHERE profile_id = :id"),
                {"id": profile_id}
            )

            await session.execute(
                text("DELETE FROM adv_uuid.profiles WHERE id = :id"),
                {"id": profile_id}
            )

            await session.commit()
            print(f"✅ Удален пользователь из БД: {profile_id}")

        except Exception as e:
            await session.rollback()
            print(f"⚠️ Не удалось удалить пользователя {profile_id}: {e}")


class UserRepositoryResponseBuilder:
    """Builder для ответов репозитория User (для моков)"""

    @staticmethod
    def create_success_response(user_data: Dict[str, Any] = None):
        """Создает успешный ответ репозитория"""
        if user_data is None:
            user_data = {}

        builder = UserBuilder()
        for key, value in user_data.items():
            if hasattr(builder, f"with_{key}"):
                getattr(builder, f"with_{key}")(value)

        return builder.build()

    @staticmethod
    def create_user_not_found_response():
        """Создает ответ 'пользователь не найден'"""
        return None

    @staticmethod
    def create_user_list_response(count: int = 3):
        """Создает список пользователей"""
        return [UserBuilder().build() for _ in range(count)]