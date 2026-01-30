import uuid
from faker import Faker
from typing import Dict, Any
from datetime import datetime, timezone

fake = Faker()


class AdvertBuilder:
    """Data Builder для создания объектов Advert"""

    def __init__(self):
        self.advert_data = {
            "id": uuid.uuid4(),
            "content": fake.text(),
            "description": fake.text(),
            "id_category": uuid.uuid4(),
            "price": fake.random_int(min=100, max=100000),
            "id_seller": uuid.uuid4(),
            "date_created": datetime.now(timezone.utc)
        }

    def with_id(self, advert_id: uuid.UUID) -> 'AdvertBuilder':
        self.advert_data["id"] = advert_id
        return self

    def with_content(self, content: str) -> 'AdvertBuilder':
        self.advert_data["content"] = content
        return self

    def with_description(self, description: str) -> 'AdvertBuilder':
        self.advert_data["description"] = description
        return self

    def with_title(self, title: str) -> 'AdvertBuilder':
        """Alias for content (since content seems to be the title field)"""
        self.advert_data["content"] = title
        return self

    def with_price(self, price: int) -> 'AdvertBuilder':
        """Price must be integer"""
        self.advert_data["price"] = int(price)
        return self

    def with_user_id(self, user_id: uuid.UUID) -> 'AdvertBuilder':
        """Для user_id используем id_seller"""
        self.advert_data["id_seller"] = user_id
        return self

    def with_category_id(self, category_id: uuid.UUID) -> 'AdvertBuilder':
        """Для category_id используем id_category"""
        self.advert_data["id_category"] = category_id
        return self

    def with_date_created(self, date_created: datetime) -> 'AdvertBuilder':
        self.advert_data["date_created"] = date_created
        return self

    def build(self):
        from models.advert import Advert
        return Advert(**self.advert_data)


class AdvertUpdateBuilder:
    """Data Builder для создания объектов AdvertUpdatePartialDTO"""

    def __init__(self):
        self.update_data = {}

    def with_title(self, title: str) -> 'AdvertUpdateBuilder':
        """Для обновления title используем content"""
        self.update_data["content"] = title
        return self

    def with_description(self, description: str) -> 'AdvertUpdateBuilder':
        self.update_data["description"] = description
        return self

    def with_price(self, price: int) -> 'AdvertUpdateBuilder':
        self.update_data["price"] = int(price)
        return self

    def with_category_id(self, category_id: uuid.UUID) -> 'AdvertUpdateBuilder':
        self.update_data["category_id"] = category_id
        return self

    def with_content(self, content: str) -> 'AdvertUpdateBuilder':
        self.update_data["content"] = content
        return self

    def build(self):
        from api_v1.dto.advert_dto import AdvertUpdatePartialDTO
        return AdvertUpdatePartialDTO(**self.update_data)


class AdvertMother:
    """Object Mother pattern для стандартных сценариев"""

    @staticmethod
    def create_valid_advert():
        """Создает валидное объявление"""
        return AdvertBuilder().build()

    @staticmethod
    def create_advert_with_user(user_id: uuid.UUID):
        """Создает объявление с конкретным пользователем"""
        return AdvertBuilder().with_user_id(user_id).build()

    @staticmethod
    def create_advert_with_category(category_id: uuid.UUID):
        """Создает объявление с конкретной категорией"""
        return AdvertBuilder().with_category_id(category_id).build()

    @staticmethod
    def create_expensive_advert():
        """Создает дорогое объявление"""
        return AdvertBuilder().with_price(10000).build()

    @staticmethod
    def create_cheap_advert():
        """Создает дешевое объявление"""
        return AdvertBuilder().with_price(100).build()

    @staticmethod
    def create_advert_with_title(title: str):
        """Создает объявление с конкретным заголовком (content)"""
        return AdvertBuilder().with_content(title).build()

    @staticmethod
    def create_advert_with_keyword(keyword: str):
        """Создает объявление с ключевым словом в заголовке (content)"""
        return AdvertBuilder().with_content(f"Advert with {keyword}").build()


class AdvertRepositoryResponseBuilder:
    """Builder для ответов репозитория (для моков)"""

    @staticmethod
    def create_success_response(advert_data: Dict[str, Any] = None):
        """Создает успешный ответ репозитория"""
        if advert_data is None:
            advert_data = {}
        builder = AdvertBuilder()
        for key, value in advert_data.items():
            if hasattr(builder, f"with_{key}"):
                getattr(builder, f"with_{key}")(value)
        return builder.build()

    @staticmethod
    def create_list_response(count: int = 2):
        """Создает список объявлений"""
        return [AdvertBuilder().build() for _ in range(count)]

    @staticmethod
    def create_empty_list_response():
        """Создает пустой список"""
        return []