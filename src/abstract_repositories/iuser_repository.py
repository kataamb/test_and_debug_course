from abc import ABC, abstractmethod
from uuid import UUID
from models.user import User
from typing import Optional

class IUserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User: ...

    @abstractmethod
    async def delete(self, profile_id: UUID) -> bool: ...

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[User]: ...