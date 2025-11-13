from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from service_locator import get_locator, ServiceLocator
from dto.advert_dto import AdvertWithCategoryDTO
from uuid import UUID

templates = Jinja2Templates(directory="templates")
main_router = APIRouter()


@main_router.get("/", response_class=HTMLResponse)
async def index(request: Request, locator: ServiceLocator = Depends(get_locator)):
    user_id = request.state.user["id"] if request.state.user else None

    categories = await locator.category_service().get_all()
    print(categories)
    adverts_dto = []

    adverts = await locator.advert_service().get_all_adverts()
    for advert in adverts:
        dto = AdvertWithCategoryDTO(**advert.model_dump())
        dto.category_name = await locator.category_service().get_name_by_id(dto.id_category)

        if user_id:
            dto.is_favorite = await locator.liked_service().is_liked(user_id, dto.id)
            dto.is_bought = await locator.deals_service().is_in_deals(user_id, dto.id)
            dto.is_created = await locator.advert_service().is_created(user_id, dto.id)
            dto.is_really_bought = await locator.deals_service().is_bought(dto.id)

        adverts_dto.append(dto)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": request.state.user, "user_id": user_id, "adverts": adverts_dto, "categories": categories},
    )


@main_router.get("/category/{category_id}", response_class=HTMLResponse)
async def adverts_by_category(request: Request, category_id: UUID, locator: ServiceLocator = Depends(get_locator)):
    user_id = request.state.user["id"] if request.state.user else None

    categories = await locator.category_service().get_all()

    if request.state.user:
        adverts = await locator.advert_service().get_adverts_by_category(category_id)  # Используем обычный метод
    else:
        adverts = await locator.advert_service().get_adverts_by_category(category_id)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "user": request.state.user,
            "user_id": user_id,
            "adverts": adverts,
            "categories": categories
        },
    )


@main_router.get("/search", response_class=HTMLResponse)
async def search_adverts(request: Request, q: str, locator: ServiceLocator = Depends(get_locator)):
    adverts = await locator.advert_service().get_adverts_by_key_word(q)
    categories = await locator.category_service().get_all()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "user": request.state.user, "adverts": adverts, "categories": categories}
    )


@main_router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("profile.html", {"request": request, "user": request.state.user})