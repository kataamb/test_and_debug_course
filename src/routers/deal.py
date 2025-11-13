from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import get_locator, ServiceLocator
from uuid import UUID

templates = Jinja2Templates(directory="templates")
deals_router = APIRouter()


@deals_router.post("/deal_create/{item_id}")
async def create_deal(
        request: Request,
        item_id: UUID,
        locator: ServiceLocator = Depends(get_locator)
):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = request.state.user["id"]
    deals_service = locator.deals_service()

    try:
        await deals_service.create_deal(user_id, item_id)
        return RedirectResponse(url='/', status_code=303)  # Вернуться на главную или на страницу объявления
    except Exception as e:
        return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})


