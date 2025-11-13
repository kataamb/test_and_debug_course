from abstract_repositories.ihistory_deal_repository import IHistoryDealRepository
from models.history_deal import HistoryDeal
from typing import List

class HistoryDealService:
    def __init__(self, repo: IHistoryDealRepository):
        self.repo = repo

    async def create(self, history_deal: HistoryDeal) -> HistoryDeal:
        return await self.repo.create(history_deal)

    async def get_all(self) -> List[HistoryDeal]:
        return await self.repo.get_all()

    async def get_by_user(self, user_id):
        return await self.repo.get_by_user(user_id)
