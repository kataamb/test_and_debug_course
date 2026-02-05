from models.category import Category
from uuid import UUID

class MotherCategory:
    @staticmethod
    def default_category() -> Category:
        return Category(id=UUID(int=1), name="transport")

    @staticmethod
    def transport() -> Category:
        return Category(id= UUID(int=1), name = "transport")