from abc import ABC, abstractmethod
from typing import List, Optional
from models.advert import Advert
from api_v1.dto.advert_dto import AdvertUpdatePartialDTO
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
    async def is_created(self, user_id: UUID, advert_id: UUID) -> bool: ...

    @abstractmethod
    async def get_adverts_by_key_word(self, key_word: str) -> List[Advert]: ...

    @abstractmethod
    async def get_adverts_by_category(self, category_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def get_adverts_by_category_and_keyword(self, key_word: str, category_id: UUID) -> List[Advert]: ...

    @abstractmethod
    async def update_advert(self, advert_id: UUID, advert_data: Advert) -> Advert: ...

    @abstractmethod
    async def partial_update_advert(self, advert_id: UUID, advert_data: AdvertUpdatePartialDTO) -> Advert: ...

    @abstractmethod
    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None: ...



class AdvertService(IAdvertService):
    def __init__(self, repo: IAdvertRepository):
        self.repo = repo


    async def create_advert(self, advert: Advert) -> Optional[Advert]:
        result = await self.repo.create(advert)
        print(advert)
        print("AAAAA", result)
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

    async def get_adverts_by_category_and_keyword(self, keyword: str, category_id: UUID) -> List[Advert]:
        if not keyword and not category_id:
            return await self.repo.get_all_adverts()

        elif keyword and not category_id:
            return await self.repo.get_adverts_by_key_word(keyword)

        elif not keyword and category_id:
            return await self.repo.get_adverts_by_category(category_id)

        else:  # оба параметра заданы
            return await self.repo.get_adverts_by_category_and_keyword(keyword, category_id)

    async def update_advert(self, advert_id: UUID, advert_data: Advert) -> Advert:
        """
        Полное обновление объявления с бизнес-логикой
        """
        return await self.repo.update_advert(advert_id, advert_data)

    async def partial_update_advert(self, advert_id: UUID, advert_data: AdvertUpdatePartialDTO) -> Advert:
        """
        Частичное обновление объявления с бизнес-логикой
        """
        # Подготавливаем данные для обновления
        update_dict = {}

        if advert_data.content is not None:
            update_dict["content"] = advert_data.content

        if advert_data.description is not None:
            update_dict["description"] = advert_data.description

        if advert_data.price is not None:
            update_dict["price"] = str(advert_data.price)

        if advert_data.id_category is not None:
            update_dict["id_category"] = str(advert_data.id_category)

        return await self.repo.partial_update_advert(advert_id, update_dict)


    async def delete_advert(self, advert_id: UUID, user_id: UUID) -> None:
        advert = await self.repo.get_by_id(advert_id)
        if not advert:
            raise ValueError("Advert not found")

        await self.repo.delete_advert(user_id, advert_id)

