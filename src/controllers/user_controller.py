# controllers/user_controller.py
from __future__ import annotations

from typing import Union
from fastapi import Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import ServiceLocator

templates = Jinja2Templates(directory="templates")


class UserController:
    def __init__(self, locator: ServiceLocator) -> None:
        self.locator = locator

    async def login_page(self, request: Request) -> HTMLResponse:
        return templates.TemplateResponse("login.html", {"request": request})

    async def login(self, request: Request) -> Union[HTMLResponse, RedirectResponse]:
        service = self.locator.auth_service()
        form_data = await request.form()

        email = form_data.get("email")
        password = form_data.get("password")

        # Преобразуем в строки и проверяем на None
        email_str = str(email) if email is not None else ""
        password_str = str(password) if password is not None else ""

        try:
            token = await service.login(self.locator.session, email_str, password_str)
            response = RedirectResponse(url="/", status_code=303)
            response.set_cookie(key="access_token", value=token, httponly=True)
            return response
        except Exception as e:
            return templates.TemplateResponse("login.html", {"request": request, "error": str(e)})

    async def register_page(self, request: Request) -> HTMLResponse:
        return templates.TemplateResponse("register.html", {"request": request, "user": request.state.user})

    async def register(self, request: Request) -> Union[HTMLResponse, RedirectResponse]:
        service = self.locator.auth_service()
        form_data = await request.form()

        try:
            # Преобразуем все значения в строки
            await service.register(
                self.locator.session,
                {
                    "nickname": str(form_data.get("nickname", "")),
                    "fio": str(form_data.get("fio", "")),
                    "email": str(form_data.get("email", "")),
                    "phone_number": str(form_data.get("phone_number", "")),
                    "password": str(form_data.get("password", "")),
                    "repeat_password": str(form_data.get("repeat_password", "")),
                },
            )
            return RedirectResponse(url="/login", status_code=303)
        except Exception as e:
            return templates.TemplateResponse(
                "register.html",
                {"request": request, "user": None, "error": str(e)}
            )

    async def logout(self, request: Request) -> RedirectResponse:
        response = RedirectResponse(url="/", status_code=303)
        response.delete_cookie("access_token")
        return response