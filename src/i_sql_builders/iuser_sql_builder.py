from __future__ import annotations
from abc import ABC, abstractmethod
from uuid import UUID
from i_sql_builders.sql_types.sql_types import TextAndParams

class IUserSqlBuilder(ABC):
    @abstractmethod
    def create_user(self, user_data: dict) -> TextAndParams: ...

    @abstractmethod
    def create_customer(self, profile_id: UUID, rating: int = 0) -> TextAndParams: ...

    @abstractmethod
    def create_seller(self, profile_id: UUID, rating: int = 0) -> TextAndParams: ...

    @abstractmethod
    def delete_customer(self, profile_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def delete_seller(self, profile_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def delete_profile(self, profile_id: UUID) -> TextAndParams: ...

    @abstractmethod
    def find_by_email(self, email: str) -> TextAndParams: ...