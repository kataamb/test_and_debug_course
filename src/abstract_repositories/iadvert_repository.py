from abc import ABC, abstractmethod
from typing import List, Optional
from models.advert import Advert
from datetime import datetime
from uuid import UUID


class IAdvertRepository(ABC):
    @abstractmethod
    async def create(self, advert: Advert) -> Optional[Advert]: ...
    @abstractmethod
    async def get_by_id(self, advert_id: UUID) -> Optional[Advert]: ...
    @abstractmethod
    async def get_all_adverts(self) -> List[Advert]: ...

    @abstractmethod
    async def get_advert_by_user(self, user_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def is_created(self, user_id: UUID, advert_id: UUID) -> bool: ...

    @abstractmethod
    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]: ...

    @abstractmethod
    async def get_adverts_by_filter(self, begin_time: datetime, end_time: datetime) -> List[Advert]: ...

    @abstractmethod
    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None: ...
