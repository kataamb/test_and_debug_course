from typing import Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from abstract_repositories.iuser_repository import IUserRepository
from i_sql_builders.iuser_sql_builder import IUserSqlBuilder
from models.user import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession, builder: IUserSqlBuilder):
        self.session = session
        self.builder = builder

    async def create(self, user: User) -> User:
        try:
            # Создаём профиль
            sql, params = self.builder.create_user({
                "nickname": user.nickname,
                "fio": user.fio,
                "email": user.email,
                "phone_number": user.phone_number,
                "password": user.password
            })
            result = await self.session.execute(sql, params)
            profile_row = result.mappings().first()

            if not profile_row:
                raise SQLAlchemyError("Failed to create profile")

            profile_id = profile_row["id"]

            # Создаём customer
            sql, params = self.builder.create_customer(profile_id)
            await self.session.execute(sql, params)

            # Создаём seller
            sql, params = self.builder.create_seller(profile_id)
            await self.session.execute(sql, params)

            await self.session.commit()

            return User(
                id=profile_id,
                nickname=user.nickname,
                fio=user.fio,
                email=user.email,
                phone_number=user.phone_number,
                password=user.password
            )

        except IntegrityError as e:
            await self.session.rollback()
            raise e
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise e

    async def delete(self, profile_id: UUID) -> bool:
        try:
            sql, params = self.builder.delete_customer(profile_id)
            await self.session.execute(sql, params)

            sql, params = self.builder.delete_seller(profile_id)
            await self.session.execute(sql, params)

            sql, params = self.builder.delete_profile(profile_id)
            await self.session.execute(sql, params)

            await self.session.commit()
            return True
        except SQLAlchemyError:
            await self.session.rollback()
            return False

    async def find_by_email(self, email: str) -> Optional[User]:
        try:
            sql, params = self.builder.find_by_email(email)
            result = await self.session.execute(sql, params)
            row = result.mappings().first()
            if not row:
                return None
            return User(**row)
        except SQLAlchemyError:
            return None