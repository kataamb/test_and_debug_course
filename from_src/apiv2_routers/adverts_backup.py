from fastapi import APIRouter, Depends

from api_v2.dependencies import get_service_locator, get_optional_user
from service_locator import ServiceLocator
from api_v1.dto.advert_dto import AdvertListResponseDTO, AdvertResponseDTO

api_v2_router_adverts = APIRouter(prefix="/adverts", tags=["Adverts v2"])


@api_v2_router_adverts.get("/", response_model=AdvertListResponseDTO)
async def get_all_adverts(
        locator: ServiceLocator = Depends(get_service_locator),
        current_user: dict = Depends(get_optional_user)
):
    """Получить все объявления."""
    adverts = await locator.advert_service().get_all_adverts()

    items = []
    for advert in adverts:
        dto = AdvertResponseDTO(
            id=advert.id,
            content=advert.content,
            description=advert.description,
            price=advert.price,
            id_category=advert.id_category,
            id_seller=advert.id_seller,
            date_created=advert.date_created,
            category_name=await locator.category_service().get_name_by_id(advert.id_category),
            seller_name='',
            is_created=current_user and await locator.advert_service().is_created(current_user["id"], advert.id),
            is_liked=current_user and await locator.liked_service().is_liked(current_user["id"], advert.id),
            is_bought=await locator.deals_service().is_bought(advert.id),
            is_bought_by_current=current_user and await locator.deals_service().is_in_deals(current_user["id"],
                                                                                            advert.id),
        )
        items.append(dto)

    return AdvertListResponseDTO(items=items)