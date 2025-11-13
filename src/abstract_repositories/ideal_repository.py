from abc import ABC, abstractmethod
from typing import List
from models.advert import Advert
from models.deal import Deal
from uuid import UUID


class IDealRepository(ABC):
    @abstractmethod
    async def create_deal(self, user_id: UUID, advert_id :UUID) -> Deal: ...

    @abstractmethod
    async def get_deals_by_user(self, user_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def is_in_deals(self, user_id: UUID, advert_id: UUID) -> bool: ...

    @abstractmethod
    async def is_bought(self, advert_id: UUID) -> bool: ...