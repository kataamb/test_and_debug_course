from __future__ import annotations

from typing import List
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import ServiceLocator
from models.advert import Advert
from dto.advert_dto import AdvertWithCategoryDTO
from uuid import UUID

templates = Jinja2Templates(directory="templates")


class AdvertController:
    def __init__(self, locator: ServiceLocator) -> None:
        self.locator = locator

    async def create_advert_form(self, request: Request) -> HTMLResponse | RedirectResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)

        categories = await self.locator.category_service().get_all()
        return templates.TemplateResponse(
            "create_advert.html",
            {
                "request": request,
                "user": request.state.user,
                "categories": categories
            }
        )

    async def create_advert(self, request: Request) -> HTMLResponse | RedirectResponse:
        if not request.state.user:
            return RedirectResponse(url="/login", status_code=303)

        try:
            advert_service = self.locator.advert_service()
            form_data = await request.form()

            # Безопасное преобразование типов
            content = str(form_data.get("content", ""))
            description = str(form_data.get("description", ""))

            # Безопасное преобразование чисел с проверкой
            price_str = form_data.get("price")
            id_category_str = form_data.get("id_category")

            # Преобразуем в int только если значения существуют и являются цифрами
            price = int(str(price_str)) if str(price_str) and str(price_str).isdigit() else 0
            id_category = UUID(str(id_category_str))

            advert_obj = Advert(
                content=content,
                description=description,
                id_category=id_category,
                price=price,
                id_seller=request.state.user["id"],
            )

            await advert_service.create_advert(advert_obj)
            return RedirectResponse(url="/profile/my_adverts", status_code=303)
        except ValueError as e:
            # Обработка ошибок преобразования чисел
            categories = await self.locator.category_service().get_all()
            return templates.TemplateResponse(
                "create_advert.html",
                {
                    "request": request,
                    "user": request.state.user,
                    "categories": categories,
                    "error": f"Ошибка в числовых данных: {str(e)}"
                }
            )
        except Exception as e:
            categories = await self.locator.category_service().get_all()
            return templates.TemplateResponse(
                "create_advert.html",
                {
                    "request": request,
                    "user": request.state.user,
                    "categories": categories,
                    "error": str(e)
                }
            )

    async def _create_advert_dto(self, advert: Advert, user_id: UUID | None = None) -> AdvertWithCategoryDTO:
        dto = AdvertWithCategoryDTO(**advert.model_dump())
        dto.category_name = await self.locator.category_service().get_name_by_id(dto.id_category)

        if user_id:
            dto.is_favorite = await self.locator.liked_service().is_liked(user_id, dto.id)
            dto.is_bought = await self.locator.deals_service().is_in_deals(user_id, dto.id)
            dto.is_created = await self.locator.advert_service().is_created(user_id, dto.id)
            dto.is_really_bought = await self.locator.deals_service().is_bought(dto.id)

        return dto

    async def get_adverts_with_dto(self, adverts: List[Advert], user_id: UUID | None = None) -> List[
        AdvertWithCategoryDTO]:
        adverts_dto = []
        for advert in adverts:
            dto = await self._create_advert_dto(advert, user_id)
            adverts_dto.append(dto)
        return adverts_dto