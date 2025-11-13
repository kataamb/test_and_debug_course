from __future__ import annotations
from uuid import UUID
from sqlalchemy import text
from i_sql_builders.iuser_sql_builder import IUserSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams

class UserSqlBuilder(IUserSqlBuilder):
    def create_user(self, user_data: dict) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.profiles (nickname, fio, email, phone_number, password)
            VALUES (:nickname, :fio, :email, :phone_number, :password)
            RETURNING id, nickname, fio, email, phone_number, password
        """)
        params: SqlParams = {
            "nickname": user_data["nickname"],
            "fio": user_data["fio"],
            "email": user_data["email"],
            "phone_number": user_data["phone_number"],
            "password": user_data["password"]
        }
        return sql, params

    def create_customer(self, profile_id: UUID, rating: int = 0) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.customers (profile_id, rating)
            VALUES (:profile_id, :rating)
        """)
        return sql, {"profile_id": str(profile_id), "rating": rating}

    def create_seller(self, profile_id: UUID, rating: int = 0) -> TextAndParams:
        sql = text("""
            INSERT INTO adv_uuid.sellers (profile_id, rating)
            VALUES (:profile_id, :rating)
        """)
        return sql, {"profile_id": str(profile_id), "rating": rating}

    def delete_customer(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM adv_uuid.customers WHERE profile_id = :id"), {"id": str(profile_id)}

    def delete_seller(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM adv_uuid.sellers WHERE profile_id = :id"), {"id": str(profile_id)}

    def delete_profile(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM adv_uuid.profiles WHERE id = :id"), {"id": str(profile_id)}

    def find_by_email(self, email: str) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.profiles WHERE email = :email"), {"email": email}