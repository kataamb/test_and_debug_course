from abc import ABC, abstractmethod
from models.history_deal import HistoryDeal
from i_sql_builders.sql_types.sql_types import TextAndParams
from uuid import UUID


class IHistoryDealSqlBuilder(ABC):
    @abstractmethod
    def create(self, history_deal: HistoryDeal) -> TextAndParams:
        """SQL для создания записи в истории сделок"""
        ...

    @abstractmethod
    def get_all(self) -> TextAndParams:
        """SQL для получения всех записей истории"""
        ...

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> TextAndParams:
        """SQL для истории конкретного пользователя"""
        ...
