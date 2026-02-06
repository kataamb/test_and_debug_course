# tests/fixtures/sqlite_sql_builders.py
"""SQLite-совместимые SQL builders для тестов"""
from __future__ import annotations
from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from models.advert import Advert
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from i_sql_builders.icategory_sql_builder import ICategorySqlBuilder
from i_sql_builders.iuser_sql_builder import IUserSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams


class SQLiteAdvertSqlBuilder(IAdvertSqlBuilder):
    """SQLite-совместимый builder для adverts (без схемы adv_uuid)"""

    def create(self, advert: Advert) -> TextAndParams:
        # pysqlite3 поддерживает RETURNING (SQLite 3.35.0+)
        sql = text("""
            INSERT INTO adverts (id, content, description, id_category, price, id_seller, date_created)
            VALUES (:id, :content, :description, :id_category, :price, :id_seller, :date_created)
            RETURNING id, content, description, id_category, price, id_seller, date_created
        """)
        params: SqlParams = {
            "id": str(advert.id),
            "content": advert.content,
            "description": advert.description,
            "id_category": str(advert.id_category),
            "price": advert.price,
            "id_seller": str(advert.id_seller),  # В тестах это будет seller.id
            "date_created": advert.date_created,
        }
        return sql, params

    def get_by_id(self, advert_id: UUID) -> TextAndParams:
        return text("SELECT * FROM adverts WHERE id = :id"), {"id": str(advert_id)}

    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM adverts ORDER BY date_created DESC"), {}

    def get_by_user(self, user_id: UUID) -> TextAndParams:
        # В тестах user_id - это seller.id, так как мы используем seller_id напрямую
        return (
            text('''SELECT ad.id, ad.content, ad.description, ad.id_category, ad.price, ad.id_seller, ad.date_created
            FROM adverts as ad 
            WHERE ad.id_seller = :user_id ORDER BY date_created DESC'''),
            {"user_id": str(user_id)},
        )

    def is_created(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        # В тестах user_id - это seller.id
        return (
            text('''SELECT 1 
            FROM adverts as ad
            WHERE ad.id_seller = :uid AND ad.id = :aid LIMIT 1'''),
            {"uid": str(user_id), "aid": str(advert_id)},
        )

    def search_by_keyword(self, keyword_like: str) -> TextAndParams:
        # SQLite не поддерживает функции, используем простой LIKE
        return text("SELECT * FROM adverts WHERE content LIKE :kw OR description LIKE :kw"), {"kw": keyword_like}

    def filter_by_dates(self, begin: datetime, end: datetime) -> TextAndParams:
        sql = text("""
            SELECT * FROM adverts 
            WHERE date_created BETWEEN :begin_time AND :end_time
            ORDER BY date_created DESC
        """)
        return sql, {"begin_time": begin, "end_time": end}

    def by_category(self, category_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adverts WHERE id_category = :category_id ORDER BY date_created DESC"),
            {"category_id": str(category_id)},
        )

    def by_category_and_keyword(self, keyword_like: str, category_id: UUID) -> TextAndParams:
        return (
            text(
                "SELECT * FROM adverts WHERE id_category = :category_id AND (content LIKE :kw OR description LIKE :kw) ORDER BY date_created DESC"),
            {"category_id": str(category_id), "kw": keyword_like},
        )

    def update_full(self, advert_id: UUID, advert: Advert) -> TextAndParams:
        # pysqlite3 поддерживает RETURNING (SQLite 3.35.0+)
        sql = text("""
            UPDATE adverts 
            SET content = :content, 
                description = :description, 
                id_category = :id_category, 
                price = :price
            WHERE id = :advert_id
            RETURNING id, content, description, id_category, price, id_seller, date_created
        """)
        params: SqlParams = {
            "advert_id": str(advert_id),
            "content": advert.content,
            "description": advert.description,
            "id_category": str(advert.id_category),
            "price": advert.price
        }
        return sql, params

    def update_partial(self, advert_id: UUID, update_data: dict) -> TextAndParams:
        set_parts = []
        params: SqlParams = {"advert_id": str(advert_id)}

        if "content" in update_data:
            set_parts.append("content = :content")
            params["content"] = update_data["content"]

        if "description" in update_data:
            set_parts.append("description = :description")
            params["description"] = update_data["description"]

        if "price" in update_data:
            set_parts.append("price = :price")
            params["price"] = update_data["price"]

        if "id_category" in update_data:
            set_parts.append("id_category = :id_category")
            params["id_category"] = str(update_data["id_category"])

        if not set_parts:
            raise ValueError("No fields to update")

        # pysqlite3 поддерживает RETURNING (SQLite 3.35.0+)
        sql = text(f"""
            UPDATE adverts 
            SET {', '.join(set_parts)}
            WHERE id = :advert_id
            RETURNING id, content, description, id_category, price, id_seller, date_created
        """)

        return sql, params

    def delete(self, advert_id: UUID, user_id: UUID) -> TextAndParams:
        return (
            text("DELETE FROM adverts WHERE id = :advert_id AND id_seller = :user_id"),
            {"advert_id": str(advert_id), "user_id": str(user_id)},
        )


class SQLiteCategorySqlBuilder(ICategorySqlBuilder):
    """SQLite-совместимый builder для categories"""

    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM categories"), {}

    def get_name_by_id(self, id_category: UUID) -> TextAndParams:
        return text("SELECT name FROM categories WHERE id = :id"), {"id": str(id_category)}


class SQLiteUserSqlBuilder(IUserSqlBuilder):
    """SQLite-совместимый builder для users"""

    def create_user(self, user_data: dict) -> TextAndParams:
        # pysqlite3 поддерживает RETURNING (SQLite 3.35.0+)
        sql = text("""
            INSERT INTO profiles (id, nickname, fio, email, phone_number, password)
            VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
            RETURNING id, nickname, fio, email, phone_number, password
        """)
        params: SqlParams = {
            "id": str(user_data.get("id", "")),
            "nickname": user_data["nickname"],
            "fio": user_data["fio"],
            "email": user_data["email"],
            "phone_number": user_data["phone_number"],
            "password": user_data["password"]
        }
        return sql, params

    def create_customer(self, profile_id: UUID, rating: int = 0) -> TextAndParams:
        sql = text("""
            INSERT INTO customers (id, profile_id, rating)
            VALUES (:id, :profile_id, :rating)
        """)
        return sql, {"id": str(UUID(int=0)), "profile_id": str(profile_id), "rating": rating}

    def create_seller(self, profile_id: UUID, rating: int = 0) -> TextAndParams:
        sql = text("""
            INSERT INTO sellers (id, profile_id, rating)
            VALUES (:id, :profile_id, :rating)
        """)
        return sql, {"id": str(UUID(int=0)), "profile_id": str(profile_id), "rating": rating}

    def delete_customer(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM customers WHERE profile_id = :id"), {"id": str(profile_id)}

    def delete_seller(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM sellers WHERE profile_id = :id"), {"id": str(profile_id)}

    def delete_profile(self, profile_id: UUID) -> TextAndParams:
        return text("DELETE FROM profiles WHERE id = :id"), {"id": str(profile_id)}

    def find_by_email(self, email: str) -> TextAndParams:
        return text("SELECT * FROM profiles WHERE email = :email"), {"email": email}
