# routes/likes.py
from fastapi import APIRouter, Depends, status
from uuid import UUID

from api_v1.dto.like_dto import *
from api_v1.errors.errors import (
    AdvertNotFoundError, LikeAlreadyExistsError, LikeNotFoundError,
    AuthorizationError, DatabaseError
)

from service_locator import get_locator, ServiceLocator
from core.create_jwt import get_current_user

api_v1_likes_router = APIRouter(prefix="/api/v1/adverts", tags=["Likes"])


@api_v1_likes_router.post(
    "/{advert_id}/likes",
    response_model=LikeResponseDTO,
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"description": "Like added successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_403_FORBIDDEN: {"description": "Cannot like own advert"},
        status.HTTP_404_NOT_FOUND: {"description": "Advert not found"},
        status.HTTP_409_CONFLICT: {"description": "Like already exists"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def add_like(
        advert_id: UUID,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Like an advert
    """
    try:
        likes_service = locator.liked_service()
        advert_service = locator.advert_service()

        # Проверяем существование объявления
        advert = await advert_service.get_advert(advert_id)
        if not advert:
            raise AdvertNotFoundError()

        # Проверяем, не является ли пользователь владельцем объявления
        if advert.id_seller == current_user["id"]:
            raise AuthorizationError("You cannot like your own advert")

        # TODO: Проверяем, не поставлен ли уже лайк
        existing_like = await likes_service.is_liked(advert_id, current_user["id"])
        if existing_like:
             raise LikeAlreadyExistsError()

        # Добавляем лайк

        liked = await likes_service.add_to_liked(advert_id, current_user["id"])
        return LikeListResponseDTO(
            id = liked.id,
            advert_id = liked.id_advert,
            customer_id = liked.id_customer,
        )

    except (AdvertNotFoundError, AuthorizationError, LikeAlreadyExistsError):
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to add like: {str(e)}")


@api_v1_likes_router.delete(
    "/{advert_id}/likes",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={
        status.HTTP_204_NO_CONTENT: {"description": "Like removed successfully"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_404_NOT_FOUND: {"description": "Like not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def remove_like(
        advert_id: UUID,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Remove like from advert
    """
    try:
        likes_service = locator.liked_service()

        like = await likes_service.is_liked(advert_id, current_user["id"])
        if not like:
             raise LikeNotFoundError()

        # Удаляем лайк
        await likes_service.remove_from_liked(advert_id, current_user["id"])

    except LikeNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to remove like: {str(e)}")