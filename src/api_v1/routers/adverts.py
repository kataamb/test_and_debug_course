from fastapi import APIRouter, Depends, status
from fastapi import HTTPException
from uuid import UUID
from fastapi.responses import JSONResponse

from api_v1.dto.advert_dto import (
    AdvertCreateDTO,
    AdvertUpdateFullDTO,
    AdvertUpdatePartialDTO,
    AdvertResponseDTO,
    AdvertListResponseDTO,
    AdvertSearchRequestDTO,
)
from api_v1.errors.errors import (
    AdvertNotFoundError,
    CategoryNotFoundError,
    ValidationError, DatabaseError,
    AuthorizationError
)
from core.create_jwt import *


from service_locator import get_locator, ServiceLocator

# Предполагаемая структура моделей - замени на свои
from models.advert import Advert

api_v1_adverts_router = APIRouter(prefix="/adverts", tags=["Adverts"])


@api_v1_adverts_router.get("/", response_model=AdvertListResponseDTO,
                           responses = {
                               status.HTTP_400_BAD_REQUEST: {"description": "Validation error"},
                               status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
                               status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"},
                               status.HTTP_404_NOT_FOUND: {"description": "Advert or category not found"},
                               status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
                           }
                           )
async def get_all_adverts(
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_optional_user)
):
    """
    Get all adverts 
    """
    try:
        advert_service = locator.advert_service()
        adverts = await advert_service.get_all_adverts()

        print(adverts)

        items = []
        for advert in adverts:
            # Получаем дополнительные данные для DTO
            #category_name = await locator.category_service().get_name_by_id(advert.id_category)

            advert_dto = AdvertResponseDTO(
                id=advert.id,
                content=advert.content,  # content как title
                description=advert.description,
                price=advert.price,
                id_category=advert.id_category,  # id_category как category_id
                id_seller=advert.id_seller,  # id_seller как seller_id
                date_created=advert.date_created,  # date_created как created_at
                category_name=await locator.category_service().get_name_by_id(advert.id_category),
                seller_name='',
                is_created=await locator.advert_service().is_created(current_user["id"] if current_user else None,
                                                                     advert.id),
                is_liked=await locator.liked_service().is_liked(current_user["id"] if current_user else None,
                                                                advert.id),
                is_bought=await locator.deals_service().is_bought(advert.id),
                is_bought_by_current=await locator.deals_service().is_in_deals(
                    current_user["id"] if current_user else None,
                    advert.id),
            )
            items.append(advert_dto)

        return AdvertListResponseDTO(items=items)
    
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve adverts: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating advert: {str(e)}"
        )

@api_v1_adverts_router.post("/", response_model=AdvertResponseDTO, status_code=status.HTTP_201_CREATED)
async def create_advert(
        advert_data: AdvertCreateDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    try:
        # Проверяем существование категории
        advert_service = locator.advert_service()
        deals_service = locator.deals_service()
        advert_obj = Advert(
                content=advert_data.content,
                description=advert_data.description,
                id_category=advert_data.id_category,
                price=advert_data.price,
                id_seller=current_user["id"],
            )
        advert = await advert_service.create_advert(advert_obj)
        print(advert)

        advert_dto = AdvertResponseDTO(
            id=advert.id,
            content=advert.content,  # content как title
            description=advert.description,
            price=advert.price,
            id_category=advert.id_category,  # id_category как category_id
            id_seller=advert.id_seller,  # id_seller как seller_id
            date_created=advert.date_created,  # date_created как created_at
            category_name=await locator.category_service().get_name_by_id(advert.id_category),
            seller_name='',
            is_created=await locator.advert_service().is_created(current_user["id"] if current_user else None,
                                                                 advert.id),
            is_liked=await locator.liked_service().is_liked(current_user["id"] if current_user else None,
                                                            advert.id),
            is_bought=await locator.deals_service().is_bought(advert.id),
            is_bought_by_current=await locator.deals_service().is_in_deals(current_user["id"] if current_user else None,
                                                                           advert.id),
        )

        return advert_dto

    except CategoryNotFoundError:
        raise
    except ValidationError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to create advert: {str(e)}")


@api_v1_adverts_router.post("/search", response_model=AdvertListResponseDTO,
                           responses={
                               status.HTTP_400_BAD_REQUEST: {"description": "Validation error"},
                               status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
                               status.HTTP_403_FORBIDDEN: {"description": "Not enough permissions"},
                               status.HTTP_404_NOT_FOUND: {"description": "Advert or category not found"},
                               status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
                           }
                           )
async def get_search_adverts(
        search_data: AdvertSearchRequestDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_optional_user)
):
    """
    Get all adverts
    """
    try:
        advert_service = locator.advert_service()

        adverts = await advert_service.get_adverts_by_category_and_keyword(search_data.query, search_data.id_category)
        print(search_data.query == True, search_data.id_category == True)

        items = []
        for advert in adverts:
            # Получаем дополнительные данные для DTO
            # category_name = await locator.category_service().get_name_by_id(advert.id_category)

            advert_dto = AdvertResponseDTO(
                id=advert.id,
                content=advert.content,  # content как title
                description=advert.description,
                price=advert.price,
                id_category=advert.id_category,  # id_category как category_id
                id_seller=advert.id_seller,  # id_seller как seller_id
                date_created=advert.date_created,  # date_created как created_at
                category_name=await locator.category_service().get_name_by_id(advert.id_category),
                seller_name='',
                is_created=await locator.advert_service().is_created(current_user["id"] if current_user else None,
                                                                     advert.id),
                is_liked=await locator.liked_service().is_liked(current_user["id"] if current_user else None,
                                                                advert.id),
                is_bought=await locator.deals_service().is_bought(advert.id),
                is_bought_by_current=await locator.deals_service().is_in_deals(
                    current_user["id"] if current_user else None,
                    advert.id),
            )
            items.append(advert_dto)

        return AdvertListResponseDTO(items=items)

    except Exception as e:
        raise DatabaseError(f"Failed to retrieve adverts: {str(e)}")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating advert: {str(e)}"
        )




@api_v1_adverts_router.options("/created")
async def options_created():
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Methods": "GET, OPTIONS",
            "Access-Control-Allow-Headers": "Authorization, Content-Type",
            "Access-Control-Allow-Credentials": "true",
        }
    )


@api_v1_adverts_router.get("/created", response_model=AdvertListResponseDTO)
async def get_my_adverts(
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Get all adverts my created
    """
    try:
        advert_service = locator.advert_service()
        adverts = await advert_service.get_advert_by_user(current_user["id"])

        print(adverts)

        items = []
        for advert in adverts:
            # Получаем дополнительные данные для DTO

            advert_dto = AdvertResponseDTO(
                id=advert.id,
                content=advert.content,  # content как title
                description=advert.description,
                price=advert.price,
                id_category=advert.id_category,  # id_category как category_id
                id_seller=advert.id_seller,  # id_seller как seller_id
                date_created=advert.date_created,  # date_created как created_at
                category_name=await locator.category_service().get_name_by_id(advert.id_category),
                seller_name='',
                is_created = True,
                is_liked=await locator.liked_service().is_liked(current_user["id"] if current_user else None,
                                                                advert.id),
                is_bought=await locator.deals_service().is_bought(advert.id),
                is_bought_by_current=await locator.deals_service().is_in_deals(current_user["id"] if current_user else None, advert.id),
            )
            items.append(advert_dto)


        return AdvertListResponseDTO(items=items)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating advert: {str(e)}"
        )


@api_v1_adverts_router.get(
    "/liked",
    response_model=AdvertListResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Successful response"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def get_liked_adverts(
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Get all adverts liked
    """
    try:
        liked_service = locator.liked_service()
        adverts = await liked_service.get_liked_by_user(current_user["id"])

        items = []
        for advert in adverts:
            advert_dto = AdvertResponseDTO(
                id=advert.id,
                content=advert.content,
                description=advert.description,
                price=advert.price,
                id_category=advert.id_category,
                id_seller=advert.id_seller,
                date_created=advert.date_created,
                category_name=await locator.category_service().get_name_by_id(advert.id_category),
                seller_name='',
                is_created=True,
                is_liked=True,  # раз в избранном, значит лайк есть
                is_bought=await locator.deals_service().is_bought(advert.id),
                is_bought_by_current=await locator.deals_service().is_in_deals(current_user["id"], advert.id),
            )
            items.append(advert_dto)

        return AdvertListResponseDTO(items=items)

    except Exception as e:
        raise DatabaseError(f"Failed to retrieve liked adverts: {str(e)}")

@api_v1_adverts_router.get(
    "/deals",
    response_model=AdvertListResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Successful response"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Authentication required"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def get_in_deals_adverts(
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Get all adverts in deals
    """
    try:
        deals_service = locator.deals_service()
        adverts = await deals_service.get_deals_by_user(current_user["id"])

        items = []
        for advert in adverts:
            advert_dto = AdvertResponseDTO(
                id=advert.id,
                content=advert.content,
                description=advert.description,
                price=advert.price,
                id_category=advert.id_category,
                id_seller=advert.id_seller,
                date_created=advert.date_created,
                category_name=await locator.category_service().get_name_by_id(advert.id_category),
                seller_name='',
                is_created=await locator.advert_service().is_created(current_user["id"], advert.id),
                is_liked=await locator.liked_service().is_liked(current_user["id"], advert.id),
                is_bought=True,  # раз в сделках, значит куплено
                is_bought_by_current=True,  # раз в сделках пользователя, значит текущий участвует
            )
            items.append(advert_dto)

        return AdvertListResponseDTO(items=items)

    except Exception as e:
        raise DatabaseError(f"Failed to retrieve deals adverts: {str(e)}")

@api_v1_adverts_router.get("/{advert_id}", response_model=AdvertResponseDTO)
async def get_advert(
        advert_id: UUID,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_optional_user)
):
    """
    Get advert by ID
    """
    try:
        advert_service = locator.advert_service()
        advert = await advert_service.get_advert(advert_id)

        if not advert:
            raise AdvertNotFoundError()

        # Собираем DTO с дополнительными полями
        advert_dto = AdvertResponseDTO(
            id=advert.id,
            content=advert.content,
            description=advert.description,
            price=advert.price,
            id_category=advert.id_category,
            id_seller=advert.id_seller,
            date_created=advert.date_created,
            category_name=await locator.category_service().get_name_by_id(advert.id_category),
            seller_name='',  # TODO: получить имя продавца
            is_created=await locator.advert_service().is_created(
                current_user["id"] if current_user else None, advert.id
            ),
            is_liked=await locator.liked_service().is_liked(
                current_user["id"] if current_user else None, advert.id
            ),
            is_bought=await locator.deals_service().is_bought(advert.id),
            is_bought_by_current=await locator.deals_service().is_in_deals(
                current_user["id"] if current_user else None, advert.id
            ),
        )
        return advert_dto

    except AdvertNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve advert: {str(e)}")

@api_v1_adverts_router.put("/{advert_id}", response_model=AdvertResponseDTO)
async def update_advert_full(
        advert_id: UUID,
        advert_data: AdvertUpdateFullDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Update advert (full update) - только для владельца
    """
    try:
        advert_service = locator.advert_service()

        # Проверяем существование объявления
        existing_advert = await advert_service.get_advert(advert_id)
        if not existing_advert:
            raise AdvertNotFoundError()



        advert_obj = Advert(
            content=advert_data.content,  # маппинг title → content
            description=advert_data.description,
            price=advert_data.price,
            id_category=advert_data.id_category,
            id_seller=current_user["id"]
        )
        # Обновляем объявление
        updated_advert = await advert_service.update_advert(advert_id, advert_obj)

        # Собираем ответ
        advert_dto = AdvertResponseDTO(
            id=updated_advert.id,
            content=updated_advert.content,
            description=updated_advert.description,
            price=updated_advert.price,
            id_category=updated_advert.id_category,
            id_seller=updated_advert.id_seller,
            date_created=updated_advert.date_created,
            category_name=await locator.category_service().get_name_by_id(updated_advert.id_category),
            seller_name='',
            is_created=True,
            is_liked=await locator.liked_service().is_liked(current_user["id"], updated_advert.id),
            is_bought=await locator.deals_service().is_bought(updated_advert.id),
            is_bought_by_current=await locator.deals_service().is_in_deals(current_user["id"], updated_advert.id),
        )
        return advert_dto

    except ValidationError:
        # 400 - Bad Request (валидация)
        raise
    except AdvertNotFoundError:
        # 404 - Not Found
        raise
    except CategoryNotFoundError:
        # 404 - Not Found (категория)
        raise
    except AuthorizationError:
        # 403 - Forbidden (не владелец)
        raise
    except Exception as e:
        # 500 - Internal Server Error
        raise DatabaseError(f"Failed to update advert: {str(e)}")

@api_v1_adverts_router.patch("/{advert_id}", response_model=AdvertResponseDTO)
async def update_advert_partial(
        advert_id: UUID,
        advert_data: AdvertUpdatePartialDTO,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Update advert (partial update) - только для владельца
    """
    try:
        advert_service = locator.advert_service()

        # Проверяем существование объявления
        existing_advert = await advert_service.get_advert(advert_id)
        if not existing_advert:
            raise AdvertNotFoundError()


        # Валидация данных

        # Частичное обновление
        updated_advert = await advert_service.partial_update_advert(advert_id, advert_data)

        # Собираем ответ
        advert_dto = AdvertResponseDTO(
            id=updated_advert.id,
            content=updated_advert.content,
            description=updated_advert.description,
            price=updated_advert.price,
            id_category=updated_advert.id_category,
            id_seller=updated_advert.id_seller,
            date_created=updated_advert.date_created,
            category_name=await locator.category_service().get_name_by_id(updated_advert.id_category),
            seller_name='',
            is_created=True,
            is_liked=await locator.liked_service().is_liked(current_user["id"], updated_advert.id),
            is_bought=await locator.deals_service().is_bought(updated_advert.id),
            is_bought_by_current=await locator.deals_service().is_in_deals(current_user["id"], updated_advert.id),
        )
        return advert_dto

    except ValidationError:
        # 400 - Bad Request
        raise
    except AdvertNotFoundError:
        # 404 - Not Found
        raise
    except CategoryNotFoundError:
        # 404 - Not Found (категория)
        raise
    except AuthorizationError:
        # 403 - Forbidden
        raise
    except Exception as e:
        # 500 - Internal Server Error
        raise DatabaseError(f"Failed to update advert: {str(e)}")

@api_v1_adverts_router.delete("/{advert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_advert(
        advert_id: UUID,
        locator: ServiceLocator = Depends(get_locator),
        current_user: dict = Depends(get_current_user)
):
    """
    Delete advert - только для владельца
    """
    try:
        advert_service = locator.advert_service()

        # Проверяем существование объявления
        existing_advert = await advert_service.get_advert(advert_id)
        if not existing_advert:
            raise AdvertNotFoundError()

        # Проверяем права


        # Удаляем объявление
        await advert_service.delete_advert(advert_id, current_user["id"])

    except AdvertNotFoundError:
        # 404 - Not Found
        raise
    except AuthorizationError:
        # 403 - Forbidden
        raise
    except Exception as e:
        # 500 - Internal Server Error
        raise DatabaseError(f"Failed to delete advert: {str(e)}")


