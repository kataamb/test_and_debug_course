from __future__ import annotations

from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import ServiceLocator

from controllers.advert_controller import AdvertController
from uuid import UUID

templates = Jinja2Templates(directory="templates")


class MainController:
    def __init__(self, locator: ServiceLocator) -> None:
        self.locator = locator
        self.advert_controller = AdvertController(locator)

    async def index(self, request: Request) -> HTMLResponse:
        user_id = request.state.user["id"] if request.state.user else None
        categories = await self.locator.category_service().get_all()

        adverts = await self.locator.advert_service().get_all_adverts()
        adverts_dto = await self.advert_controller.get_adverts_with_dto(adverts, user_id)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user": request.state.user,
                "user_id": user_id,
                "adverts": adverts_dto,
                "categories": categories
            },
        )

    async def adverts_by_category(self, request: Request, category_id: UUID) -> HTMLResponse:
        user_id = request.state.user["id"] if request.state.user else None
        categories = await self.locator.category_service().get_all()

        adverts = await self.locator.advert_service().get_adverts_by_category(category_id)
        adverts_dto = await self.advert_controller.get_adverts_with_dto(adverts, user_id)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user": request.state.user,
                "user_id": user_id,
                "adverts": adverts_dto,
                "categories": categories
            },
        )

    async def search_adverts(self, request: Request, query: str) -> HTMLResponse:
        adverts = await self.locator.advert_service().get_adverts_by_key_word(query)
        categories = await self.locator.category_service().get_all()

        adverts_dto = await self.advert_controller.get_adverts_with_dto(adverts)

        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "user": request.state.user,
                "adverts": adverts_dto,
                "categories": categories
            }
        )

    async def profile_page(self, request: Request) -> HTMLResponse | RedirectResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)
        return templates.TemplateResponse("profile.html", {"request": request, "user": request.state.user})