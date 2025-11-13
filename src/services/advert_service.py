from abc import ABC, abstractmethod
from typing import List, Optional
from models.advert import Advert
from abstract_repositories.iadvert_repository import IAdvertRepository
from uuid import UUID

class IAdvertService(ABC):
    @abstractmethod
    async def create_advert(self, advert: Advert) -> Optional[Advert]: ...

    @abstractmethod
    async def get_advert(self, advert_id: UUID) -> Optional[Advert]: ...

    @abstractmethod
    async def get_all_adverts(self) -> List[Advert]: ...

    @abstractmethod
    async def get_advert_by_user(self, user_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def is_created(self, user_id: int, advert_id: UUID) -> bool: ...

    @abstractmethod
    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]: ...

    @abstractmethod
    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None: ...



class AdvertService(IAdvertService):
    def __init__(self, repo: IAdvertRepository):
        self.repo = repo


    async def create_advert(self, advert: Advert) -> Optional[Advert]:
        result = await self.repo.create(advert)
        return result

    async def get_advert(self, advert_id: UUID) -> Optional[Advert]:
        return await self.repo.get_by_id(advert_id)

    async def get_all_adverts(self) -> List[Advert]:
        return await self.repo.get_all_adverts()

    async def get_advert_by_user(self, user_id: UUID) -> List[Advert]:
        return await self.repo.get_advert_by_user(user_id)

    async def is_created(self, user_id: UUID, advert_id: UUID) -> bool:
        return await self.repo.is_created(user_id, advert_id)

    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]:
        return await self.repo.get_adverts_by_key_word(key_word)


    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]:
        return await self.repo.get_adverts_by_category(category_id)


    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None:
        advert = await self.repo.get_by_id(advert_id)
        if not advert:
            raise ValueError("Advert not found")
        if advert.id_seller != user_id:
            raise PermissionError("Not allowed to delete this advert")
        await self.repo.delete_advert(user_id, advert_id)

