from __future__ import annotations
from abc import ABC, abstractmethod
from i_sql_builders.sql_types.sql_types import TextAndParams
from uuid import UUID

class ICategorySqlBuilder(ABC):
    @abstractmethod
    def get_all(self) -> TextAndParams: ...

    @abstractmethod
    def get_name_by_id(self, id_category: UUID) -> TextAndParams: ...