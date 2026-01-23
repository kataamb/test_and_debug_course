# routes/deals.py
from fastapi import APIRouter, Depends, status

from api_v1.dto.deal_dto import DealCreateRequestDTO, DealResponseDTO
from api_v1.errors.errors import (
    AdvertNotFoundError, AuthorizationError, DatabaseError,
    ValidationError, DealAlreadyExistsError
)
from service_locator import get_locator, ServiceLocator
from core.create_jwt import get_current_user

api_v1_deals_router = APIRouter(prefix="/api/v1/deals", tags=["Deals"])


@api_v1_deals_router.post(
    "/",
    response_model=DealResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Deal created successfully"},
        status.HTTP_400_BAD_REQUEST: {"description": "Validation error"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Cannot create deal for own advert"},
        status.HTTP_404_NOT_FOUND: {"description": "Advert not found"},
        status.HTTP_409_CONFLICT: {"description": "Deal already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def create_deal(
        deal_data: DealCreateRequestDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Create a deal
    """
    try:
        deals_service = locator.deals_service()
        advert_service = locator.advert_service()

        # Проверяем существование объявления
        advert = await advert_service.get_advert(deal_data.advert_id)
        if not advert:
            raise AdvertNotFoundError()

        # Проверяем, не является ли пользователь владельцем объявления
        if advert.id_seller == current_user["id"]:
            raise AuthorizationError("You cannot create a deal for your own advert")

        # TODO: Проверяем, не существует ли уже сделка
        # existing_deal = await deals_service.get_deal_by_advert_and_buyer(deal_data.advert_id, current_user["id"])
        # if existing_deal:
        #     raise DealAlreadyExistsError()

        # Создаем сделку
        deal = await deals_service.create_deal(current_user["id"],
            advert_id=deal_data.advert_id,
        )


        return DealResponseDTO(
            id=deal.id,
            advert_id=deal.id_advert,
            customer_id=deal.id_customer,

        )

    except (AdvertNotFoundError, AuthorizationError, DealAlreadyExistsError, ValidationError):
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to create deal: {str(e)}")

