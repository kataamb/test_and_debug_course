from __future__ import annotations

from typing import Union
from fastapi import Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from service_locator import ServiceLocator
from uuid import UUID

templates = Jinja2Templates(directory="templates")


class DealsController:
    def __init__(self, locator: ServiceLocator) -> None:
        self.locator = locator

    async def create_deal(self, request: Request, item_id: UUID) -> Union[RedirectResponse, HTMLResponse]:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)

        user_id = request.state.user["id"]
        deals_service = self.locator.deals_service()

        try:
            await deals_service.create_deal(user_id, item_id)
            return RedirectResponse(url='/', status_code=303)
        except Exception as e:
            return templates.TemplateResponse("error.html", {"request": request, "error": str(e)})