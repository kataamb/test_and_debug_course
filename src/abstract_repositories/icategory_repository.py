from abc import ABC, abstractmethod
from models.category import Category
from typing import List
from uuid import UUID

class ICategoryRepository(ABC):

    @abstractmethod
    async def get_all(self) -> List[Category]: ...

    @abstractmethod
    async def get_name_by_id(self, id_category: UUID) -> str: ...


