# файл: routes/api_v1/advert_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List
from uuid import UUID

from service_locator import get_locator, ServiceLocator
from dto.advert_dto_v1 import (
    AdvertCreateDTO,
    AdvertUpdateDTO,
    AdvertResponseDTO,
    AdvertListResponseDTO,
    AdvertSearchRequestDTO
)
from core.create_jwt import JWTManager  # Используем твой JWTManager
from models.advert import Advert

api_v1_advert_router = APIRouter(prefix="/api/v1/adverts", tags=["Adverts"])

# Добавляем security для JWT
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Зависимость для получения текущего пользователя из JWT"""
    try:
        payload = JWTManager.decode_token(credentials.credentials)
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return {
            "id": UUID(user_id),  # Преобразуем строку в UUID
            "email": payload.get("sub"),
            "role": payload.get("role")
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


@api_v1_advert_router.get("/", response_model=AdvertListResponseDTO)
async def get_all_adverts(
        locator: ServiceLocator = Depends(get_locator)
):
    """Get all adverts - публичный доступ"""
    try:
        advert_service = locator.advert_service()
        adverts = await advert_service.get_all_adverts()

        items = []
        for advert in adverts:
            # Получаем дополнительные данные для DTO
            category_name = await locator.category_service().get_name_by_id(advert.id_category)
            seller_name = "TODO"  # TODO: получить имя продавца из сервиса пользователей

            advert_dto = AdvertResponseDTO(
                id=advert.id,
                title=advert.content,
                description=advert.description,
                price=advert.price,
                category_id=advert.id_category,
                seller_id=advert.id_seller,
                created_at=advert.date_created,
                updated_at=advert.date_created,
                category_name=category_name,
                seller_name=seller_name,
                likes_count=0,  # TODO: получить количество лайков
                is_liked=False  # TODO: проверить лайк текущего пользователя
            )
            items.append(advert_dto)

        return AdvertListResponseDTO(items=items)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching adverts: {str(e)}"
        )


@api_v1_advert_router.post("/", response_model=AdvertResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_advert(
        advert_data: AdvertCreateDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)  # Используем нашу зависимость
):
    """Create a new advert - только для авторизованных"""
    try:
        advert_service = locator.advert_service()

        # Используем ID пользователя из JWT токена
        advert_obj = Advert(
            content=advert_data.title,
            description=advert_data.description,
            price=advert_data.price,
            id_category=advert_data.category_id,
            id_seller=current_user["id"],  # Уже UUID из зависимости
        )

        created_advert = await advert_service.create_advert(advert_obj)

        # Получаем дополнительные данные для ответа
        category_name = await locator.category_service().get_name_by_id(created_advert.id_category)
        seller_name = "TODO"  # TODO: получить имя продавца

        return AdvertResponseDTO(
            id=created_advert.id,
            title=created_advert.content,
            description=created_advert.description,
            price=created_advert.price,
            category_id=created_advert.id_category,
            seller_id=created_advert.id_seller,
            created_at=created_advert.created_at,
            updated_at=created_advert.updated_at,
            category_name=category_name,
            seller_name=seller_name,
            likes_count=0,
            is_liked=False
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating advert: {str(e)}"
        )


@api_v1_advert_router.get("/{advert_id}", response_model=AdvertResponseDTO)
async def get_advert_by_id(
        advert_id: UUID,
        locator: ServiceLocator = Depends(get_locator)
):
    """Get advert by ID - публичный доступ"""
    try:
        advert_service = locator.advert_service()
        advert = await advert_service.get_advert_by_id(advert_id)

        if not advert:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Advert not found"
            )

        # Получаем дополнительные данные для DTO
        category_name = await locator.category_service().get_name_by_id(advert.id_category)
        seller_name = "TODO"  # TODO: получить имя продавца

        return AdvertResponseDTO(
            id=advert.id,
            title=advert.content,
            description=advert.description,
            price=advert.price,
            category_id=advert.id_category,
            seller_id=advert.id_seller,
            created_at=advert.created_at,
            updated_at=advert.updated_at,
            category_name=category_name,
            seller_name=seller_name,
            likes_count=0,
            is_liked=False
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching advert: {str(e)}"
        )


@api_v1_advert_router.get("/favorites", response_model=AdvertListResponseDTO)
async def get_favorite_adverts(
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """Get user's favorite adverts - только свои"""
    try:
        # TODO: Реализовать получение избранных объявлений
        # Пока возвращаем пустой список
        return AdvertListResponseDTO(items=[])

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching favorite adverts: {str(e)}"
        )


@api_v1_advert_router.post("/search", response_model=AdvertListResponseDTO)
async def search_adverts(
        search_data: AdvertSearchRequestDTO,
        locator: ServiceLocator = Depends(get_locator)
):
    """Search adverts with filters - публичный доступ"""
    try:
        # TODO: Реализовать поиск с фильтрами
        return await get_all_adverts(locator=locator)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error searching adverts: {str(e)}"
        )