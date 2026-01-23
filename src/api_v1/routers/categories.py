from fastapi import APIRouter, Depends, status
from uuid import UUID

from api_v1.dto.category_dto import CategoryResponseDTO, CategoryListResponseDTO
from api_v1.errors.errors import DatabaseError, CategoryNotFoundError
from service_locator import get_locator, ServiceLocator

api_v1_categories_router = APIRouter(prefix="/api/v1/categories", tags=["Categories"])


@api_v1_categories_router.get(
    "/",
    response_model=CategoryListResponseDTO,
    responses={
        status.HTTP_200_OK: {"description": "Successful response"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def get_all_categories(
        locator: ServiceLocator = Depends(get_locator)
):
    """
    Get all categories
    """
    try:
        category_service = locator.category_service()
        categories = await category_service.get_all()
        items = []
        for category in categories:
            category_obj = CategoryResponseDTO(
                id=category.id,
                name=category.name
            )
            items.append(category_obj)

        return CategoryListResponseDTO(items=items)

    except Exception as e:
        raise DatabaseError(f"Failed to retrieve categories: {str(e)}")


@api_v1_categories_router.get(
    "/{category_id}",
    response_model=str,
    responses={
        status.HTTP_200_OK: {"description": "Successful response"},
        status.HTTP_404_NOT_FOUND: {"description": "Category not found"},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"description": "Internal server error"}
    }
)
async def get_category(
        category_id: UUID,
        locator: ServiceLocator = Depends(get_locator)
):
    """
    Get category by ID
    """
    try:
        category_service = locator.category_service()
        category = await category_service.get_name_by_id(category_id)

        if not category:
            raise CategoryNotFoundError()



        return category

    except CategoryNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve category: {str(e)}")