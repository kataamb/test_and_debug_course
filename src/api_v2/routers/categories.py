from fastapi import APIRouter, Depends
from uuid import UUID

from api_v2.dependencies import get_service_locator
from service_locator import ServiceLocator
from api_v1.dto.category_dto import CategoryResponseDTO, CategoryListResponseDTO
from api_v1.errors.errors import DatabaseError, CategoryNotFoundError

api_v2_router_categories = APIRouter(prefix="/categories", tags=["Categories v2"])


@api_v2_router_categories.get("/", response_model=CategoryListResponseDTO)
async def get_all_categories(
    locator: ServiceLocator = Depends(get_service_locator)
):
    """Получить все категории."""
    try:
        categories = await locator.category_service().get_all()
        items = [
            CategoryResponseDTO(id=cat.id, name=cat.name)
            for cat in categories
        ]
        return CategoryListResponseDTO(items=items)
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve categories: {str(e)}")


@api_v2_router_categories.get("/{category_id}", response_model=str)
async def get_category_name(
    category_id: UUID,
    locator: ServiceLocator = Depends(get_service_locator)
):
    """Получить название категории по ID."""
    try:
        name = await locator.category_service().get_name_by_id(category_id)
        if not name:
            raise CategoryNotFoundError()
        return name
    except CategoryNotFoundError:
        raise
    except Exception as e:
        raise DatabaseError(f"Failed to retrieve category: {str(e)}")