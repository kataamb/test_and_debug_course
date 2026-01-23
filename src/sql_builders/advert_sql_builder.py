from __future__ import annotations
from datetime import datetime
from uuid import UUID
from sqlalchemy import text
from models.advert import Advert
from i_sql_builders.iadvert_sql_builder import IAdvertSqlBuilder
from i_sql_builders.sql_types.sql_types import TextAndParams, SqlParams


class AdvertsSqlBuilder(IAdvertSqlBuilder):
    def create(self, advert: Advert) -> TextAndParams:
        sql = text("""
                    INSERT INTO adv_uuid.adverts (content, description, id_category, price, id_seller)
                    SELECT :content, :description, :id_category, :price, s.id
                    FROM adv_uuid.sellers s
                    WHERE s.profile_id = :id_user
                    RETURNING id, content, description, id_category, price, id_seller, date_created;
                """)

        params: SqlParams = {
            "content": advert.content,
            "description": advert.description,
            "id_category": advert.id_category,
            "price": advert.price,
            "id_user": advert.id_seller,  # Меняем на id_user, так как в advert.id_seller хранится id_user
        }
        return sql, params

    def get_by_id(self, advert_id: UUID) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.adverts WHERE id = :id"), {"id": str(advert_id)}

    def get_all(self) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.adverts ORDER BY date_created DESC"), {}

    def get_by_user(self, user_id: UUID) -> TextAndParams:
        return (
            text('''SELECT ad.id, ad.content, ad.description, ad.id_category, ad.price, ad.id_seller, ad.date_created
            FROM  adv_uuid.adverts as ad join adv_uuid.sellers  as sel on ad.id_seller = sel.id
                WHERE sel.profile_id = :user_id ORDER BY date_created DESC'''),

            {"user_id": str(user_id)},
        )

    def is_created(self, user_id: UUID, advert_id: UUID) -> TextAndParams:
        return (
            text('''SELECT 1 
            FROM adv_uuid.adverts as ad join adv_uuid.sellers as sel on ad.id_seller = sel.id
            WHERE sel.profile_id = :uid AND ad.id = :aid LIMIT 1'''),
            {"uid": str(user_id), "aid": str(advert_id)},
        )

    def search_by_keyword(self, keyword_like: str) -> TextAndParams:
        return text("SELECT * FROM adv_uuid.search_adverts(:kw)"), {"kw": keyword_like}

    def filter_by_dates(self, begin: datetime, end: datetime) -> TextAndParams:
        sql = text("""
            SELECT * FROM adv_uuid.adverts 
            WHERE date_created BETWEEN :begin_time AND :end_time
            ORDER BY date_created DESC
        """)
        return sql, {"begin_time": begin, "end_time": end}

    def by_category(self, category_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adv_uuid.adverts WHERE id_category = :category_id ORDER BY date_created DESC"),
            {"category_id": str(category_id)},
        )

    def by_category_and_keyword(self, keyword_like: str, category_id: UUID) -> TextAndParams:
        return (
            text("SELECT * FROM adv_uuid.search_adverts(:kw) WHERE id_category = :category_id ORDER BY date_created DESC"),
            {"category_id": str(category_id), "kw": keyword_like},
        )

    def update_full(self, advert_id: UUID, advert: Advert) -> TextAndParams:
        """
        Полное обновление объявления (PUT)
        """
        sql = text("""
            UPDATE adv_uuid.adverts 
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
        """
        Частичное обновление объявления (PATCH)
        """
        # Динамически строим SET часть на основе переданных полей
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

        sql = text(f"""
            UPDATE adv_uuid.adverts 
            SET {', '.join(set_parts)}
            WHERE id = :advert_id
            RETURNING id, content, description, id_category, price, id_seller, date_created
        """)

        return sql, params

    def delete(self, advert_id: UUID, user_id: UUID) -> TextAndParams:
        return (
            text("DELETE FROM adv_uuid.adverts WHERE id = :advert_id AND id_seller = :user_id"),
            {"advert_id": str(advert_id), "user_id": str(user_id)},
        )