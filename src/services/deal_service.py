from abc import ABC, abstractmethod
from typing import List
from models.deal import Deal
from models.advert import Advert
from abstract_repositories.ideal_repository import IDealRepository
from uuid import UUID

class IDealsService(ABC):
    @abstractmethod
    async def create_deal(self, user_id: UUID, advert_id :UUID) -> Deal: ...

    @abstractmethod
    async def get_deals_by_user(self, user_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def is_in_deals(self, user_id: UUID, advert_id: UUID) -> bool: ...

    @abstractmethod
    async def is_bought(self, advert_id: UUID) -> bool: ...

class DealsService(IDealsService):
    def __init__(self, repo: IDealRepository):
        self.repo = repo

    async def create_deal(self, user_id: UUID, advert_id :UUID) -> Deal:
        result = await self.repo.create_deal(user_id, advert_id)
        return result

    async def get_deals_by_user(self, user_id: UUID) -> List[Advert]:
        return await self.repo.get_deals_by_user(user_id)

    async def is_in_deals(self, user_id: UUID, advert_id: UUID) -> bool:
        return await self.repo.is_in_deals(user_id, advert_id)


    async def is_bought(self, advert_id: UUID) -> bool:
        return await self.repo.is_bought(advert_id)





















