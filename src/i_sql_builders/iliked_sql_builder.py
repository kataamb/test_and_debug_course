from __future__ import annotations
from abc import ABC, abstractmethod
from i_sql_builders.sql_types.sql_types import TextAndParams
from uuid import UUID

class ILikedSqlBuilder(ABC):
    @abstractmethod
    def add_to_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def remove_from_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def get_liked_by_user(self, user_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def is_liked(self, user_id: UUID, advert_id: UUID) -> TextAndParams: ...