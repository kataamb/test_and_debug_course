
from tests.resources.user_test_data.mother_object_user import MotherUser
from tests.resources.category_test_data.mother_object_category import MotherCategory
from models.advert import Advert
from uuid import UUID
from datetime import datetime, timezone

class MotherAdvert:
    """Mother для товаров/объявлений - КОМПОЗИЦИЯ других Mother"""

    @staticmethod
    def smartphone():
        """Готовый смартфон от обычного пользователя в категории Электроника"""
        return Advert(
            id = UUID(int=1),
            content = "smartphone",
            description = "some description",
            id_category = MotherCategory.transport().id,
            price = 19900,
            id_seller = MotherUser.petrov_pavel().id,
            date_created = datetime.now(timezone.utc)
        )

