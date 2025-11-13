from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from service_locator import ServiceLocator
from services.history_deal_service import  HistoryDealService

templates = Jinja2Templates(directory="templates")

class HistoryDealController:
    def __init__(self, history_deal_service: HistoryDealService):
        self.locator = history_deal_service

    async def list_all(self, request: Request) -> HTMLResponse:
        deals = await self.locator.get_all()
        return templates.TemplateResponse(
            "history_deals_all.html",
            {"request": request, "user": request.state.user, "deals": deals},
        )

    async def list_user(self, request: Request) -> HTMLResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)
        deals = await self.locator.get_by_user(request.state.user["id"])
        return templates.TemplateResponse(
            "history_deals_user.html",
            {"request": request, "user": request.state.user, "deals": deals},
        )
