# controllers/likes_controller.py
from __future__ import annotations

from fastapi import Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import ServiceLocator
from uuid import UUID

templates = Jinja2Templates(directory="templates")


class LikesController:
    def __init__(self, locator: ServiceLocator) -> None:
        self.locator = locator

    async def add_like(self, request: Request, item_id: UUID) -> RedirectResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)

        user_id = request.state.user["id"]
        liked_service = self.locator.liked_service()

        try:
            await liked_service.add_to_liked(user_id, item_id)
            return RedirectResponse(url='/', status_code=303)
        except Exception:
            # Возвращаем редирект на главную вместо шаблона ошибки
            return RedirectResponse(url='/', status_code=303)

    async def remove_like(self, request: Request, item_id: UUID) -> RedirectResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)

        user_id = request.state.user["id"]
        liked_service = self.locator.liked_service()

        try:
            await liked_service.remove_from_liked(user_id, item_id)
            return RedirectResponse(url="/", status_code=303)
        except Exception:
            # Возвращаем редирект на главную вместо шаблона ошибки
            return RedirectResponse(url='/', status_code=303)