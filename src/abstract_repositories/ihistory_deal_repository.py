from abc import ABC, abstractmethod
from typing import List, Optional
from models.history_deal import HistoryDeal
from uuid import UUID

class IHistoryDealRepository(ABC):
    @abstractmethod
    async def create(self, history_deal: HistoryDeal) -> Optional[HistoryDeal]: ...

    @abstractmethod
    async def get_all(self) -> List[HistoryDeal]: ...

    @abstractmethod
    async def get_by_user(self, user_id: UUID) -> List[HistoryDeal]: ...
