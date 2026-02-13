# advert_builder.py
from models.advert import Advert
from tests.resources.advert_test_data.mother_object_advert import MotherAdvert
from uuid import UUID
from datetime import datetime


class AdvertBuilder:


    def __init__(self, base_advert=None):
        if base_advert is None:
            base_advert = MotherAdvert.smartphone()

        self.id = base_advert.id
        self.content = base_advert.content
        self.description = base_advert.description
        self.id_category = base_advert.id_category
        self.price = base_advert.price
        self.id_seller = base_advert.id_seller
        self.date_created = base_advert.date_created

    def with_id(self, id_number: int):
        self.id = UUID(int=id_number)
        return self

    def with_content(self, content: str):
        self.content = content
        return self

    def with_description(self, description: str):
        self.description = description
        return self

    def with_category_id(self, category_id: UUID):
        self.id_category = category_id
        return self

    def with_category(self, category):
        self.id_category = category.id
        return self

    def with_price(self, price: float):
        self.price = price
        return self

    def with_seller(self, seller_id: UUID):
        self.id_seller = seller_id
        return self



    def with_date_created(self, date: datetime):
        self.date_created = date
        return self

    def build(self):
        """Создает объект Advert с текущими настройками"""
        return Advert(
            id=self.id,
            content=self.content,
            description=self.description,
            id_category=self.id_category,
            price=self.price,
            id_seller=self.id_seller,
            date_created=self.date_created
        )