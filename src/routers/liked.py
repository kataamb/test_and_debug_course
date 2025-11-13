from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uuid import UUID
from service_locator import get_locator, ServiceLocator

templates = Jinja2Templates(directory="templates")
likes_router = APIRouter()


@likes_router.post("/like/{item_id}")
async def add_like(
        request: Request,
        item_id: UUID,
        locator: ServiceLocator = Depends(get_locator)
):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = request.state.user["id"]
    liked_service = locator.liked_service()

    try:
        await liked_service.add_to_liked(user_id, item_id)  # Раскомментируйте когда будет готов метод
        return RedirectResponse(url='/', status_code=303)  # Вернуться на страницу, откуда пришли
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


@likes_router.post("/unlike/{item_id}")
async def remove_like(
        request: Request,
        item_id: UUID,
        locator: ServiceLocator = Depends(get_locator)
):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = request.state.user["id"]
    liked_service = locator.liked_service()

    try:
        await liked_service.remove_from_liked(user_id, item_id)
        return RedirectResponse(url="/", status_code=303)  # Вернуться на страницу
    except Exception as e:
        # return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})
        print(e)