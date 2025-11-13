from __future__ import annotations
from abc import ABC, abstractmethod
from datetime import datetime
from uuid import UUID
from models.advert import Advert
from i_sql_builders.sql_types.sql_types import TextAndParams

class IAdvertSqlBuilder(ABC):
    @abstractmethod
    def create(self, advert: Advert) -> TextAndParams: ...

    @abstractmethod
    def get_by_id(self, advert_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def get_all(self) -> TextAndParams: ...

    @abstractmethod
    def get_by_user(self, user_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def is_created(self, user_id: UUID, advert_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def search_by_keyword(self, keyword_like: str) -> TextAndParams: ...

    @abstractmethod
    def filter_by_dates(self, begin: datetime, end: datetime) -> TextAndParams: ...

    @abstractmethod
    def by_category(self, category_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def delete(self, advert_id: UUID, user_id: UUID) -> TextAndParams: ...