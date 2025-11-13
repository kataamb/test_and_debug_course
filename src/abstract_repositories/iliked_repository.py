from abc import ABC, abstractmethod
from typing import List, Optional
from models.advert import Advert
from models.liked import Liked
from uuid import UUID


class ILikedRepository(ABC):
    @abstractmethod
    async def add_to_liked(self, id_advert: UUID, id_user: UUID) -> Optional[Liked]: ...

    @abstractmethod
    async def remove_from_liked(self, user_id: UUID, advert_id: UUID): ...

    @abstractmethod
    async def get_liked_by_user(self, id_user: UUID)-> List[Advert]: ...

    @abstractmethod
    async def is_liked(self, user_id: UUID, advert_id: UUID) -> bool: ...