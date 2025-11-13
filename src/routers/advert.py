from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import get_locator, ServiceLocator
from models.advert import Advert
from uuid import UUID

templates = Jinja2Templates(directory="templates")
advert_router = APIRouter()


@advert_router.get("/profile/create_advert", response_class=HTMLResponse)
async def create_advert_form(request: Request, locator: ServiceLocator = Depends(get_locator)):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)

    categories = await locator.category_service().get_all()
    return templates.TemplateResponse(
        "create_advert.html",
        {
            "request": request,
            "user": request.state.user,
            "categories": categories
        }
    )


@advert_router.post("/profile/create_advert")
async def create_advert(
        request: Request,
        locator: ServiceLocator = Depends(get_locator)
):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)

    try:
        advert_service = locator.advert_service()
        form_data = await request.form()

        content = str(form_data.get("content"))
        description = str(form_data.get("description"))
        price = int(str(form_data.get("price")))
        id_category = UUID(str(form_data.get("id_category")))

        advert_obj = Advert(
            content=content,
            description=description,
            id_category=id_category,
            price=price,
            id_seller=request.state.user["id"],
        )

        # Создание объявления через сервис
        await advert_service.create_advert(advert_obj)

        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        # При ошибке повторно показываем форму
        categories = await locator.category_service().get_all()
        return templates.TemplateResponse(
            "create_advert.html",
            {
                "request": request,
                "user": request.state.user,
                "categories": categories,
                "error": str(e)
            }
        )