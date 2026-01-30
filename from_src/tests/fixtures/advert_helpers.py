# tests/simple_db_helper.py
"""
Простые хелперы для создания тестовых данных ПОСЛЕДОВАТЕЛЬНО
"""
import uuid
from sqlalchemy.sql import text


class SimpleDBHelper:
    """Создает данные ПОСЛЕДОВАТЕЛЬНО, без параллельных операций"""
    
    @staticmethod
    async def create_test_advert(session):
        """
        Создает одно объявление с ВСЕМИ зависимостями.
        ВАЖНО: Все операции выполняются ПОСЛЕДОВАТЕЛЬНО.
        """
        # 1. Создаем профиль
        profile_id = uuid.uuid4()
        await session.execute(
            text("""
                INSERT INTO adv_uuid.profiles 
                (id, nickname, fio, email, phone_number, password)
                VALUES (:id, :nickname, :fio, :email, :phone_number, :password)
            """),
            {
                "id": profile_id,
                "nickname": f"user_{profile_id.hex[:8]}",
                "fio": "Тест ФИО",
                "email": f"test_{profile_id.hex[:8]}@example.com",
                "phone_number": "+79990000000",
                "password": "test123"
            }
        )
        
        # 2. Создаем продавца
        seller_id = uuid.uuid4()
        await session.execute(
            text("""
                INSERT INTO adv_uuid.sellers (id, profile_id, rating)
                VALUES (:id, :profile_id, :rating)
            """),
            {
                "id": seller_id,
                "profile_id": profile_id,
                "rating": 5
            }
        )
        
        # 3. Создаем категорию (если нужно)
        category_id = uuid.uuid4()
        try:
            await session.execute(
                text("""
                    INSERT INTO adv_uuid.categories (id, name)
                    VALUES (:id, :name)
                """),
                {
                    "id": category_id,
                    "name": "Тестовая категория"
                }
            )
        except Exception:
            pass  # Если таблицы нет, просто используем UUID
        
        # 4. Создаем объявление
        advert_id = uuid.uuid4()
        await session.execute(
            text("""
                INSERT INTO adv_uuid.adverts 
                (id, content, description, id_category, price, id_seller)
                VALUES (:id, :content, :description, :id_category, :price, :id_seller)
            """),
            {
                "id": advert_id,
                "content": "Тестовое объявление",
                "description": "Описание теста",
                "id_category": category_id,
                "price": 5000,
                "id_seller": seller_id
            }
        )
        
        # 5. КОММИТИМ ВСЕ ОДНИМ КОММИТОМ
        await session.commit()
        
        return {
            "advert_id": advert_id,
            "content": "Тестовое объявление",
            "price": 5000,
            "seller_id": seller_id,
            "profile_id": profile_id
        }