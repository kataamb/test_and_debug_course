from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from service_locator import get_locator, ServiceLocator

templates = Jinja2Templates(directory="templates")
user_router = APIRouter()


# Страница логина
@user_router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Обработка формы логина
@user_router.post("/login")
async def login(
        request: Request,
        locator: ServiceLocator = Depends(get_locator)
):
    service = locator.auth_service()
    form_data = await request.form()

    email = str(form_data.get("email"))
    password = str(form_data.get("password"))

    try:
        print(email, password)
        token = await service.login(locator.session, email, password)
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(key="access_token", value=token, httponly=True)
        print('ok')
        return response
    except Exception as e:
        print(e)
        return templates.TemplateResponse("login.html", {"request": request, "error": str(e)})


# -------------------
# Регистрация
# -------------------
@user_router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request, "user": request.state.user})


''''@user_router.post("/register")
async def register(
        request: Request,
        locator: ServiceLocator = Depends(get_locator),
):
    service = locator.auth_service()
    form_data = await request.form()
    print("^(")
    try:
        await service.register(
            locator.session,
            {
                "nickname": form_data.get("nickname"),
                "fio": form_data.get("fio"),
                "email": form_data.get("email"),
                "phone_number": form_data.get("phone_number"),
                "password": form_data.get("password"),
                "repeat_password": form_data.get("repeat_password"),
            },
        )
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print(e)
        return templates.TemplateResponse("register.html", {"request": request, "user": None, "error": str(e)})
'''

@user_router.post("/register")
async def register(
        request: Request,
        locator: ServiceLocator = Depends(get_locator),
):
    print("=== REGISTER ROUTE CALLED ===")  # Эта строка должна появиться
    service = locator.auth_service()
    form_data = await request.form()
    print("Form data:", dict(form_data))  # Проверим данные
    print("^(")
    try:
        print('here')
        await service.register(
            locator.session,
            {
                "nickname": form_data.get("nickname"),
                "fio": form_data.get("fio"),
                "email": form_data.get("email"),
                "phone_number": form_data.get("phone_number"),
                "password": form_data.get("password"),
                "repeat_password": form_data.get("repeat_password"),
            },
        )
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        print("Error in register:", e)
        return templates.TemplateResponse("register.html", {"request": request, "user": None, "error": str(e)})


# -------------------
# Логаут
# -------------------
@user_router.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response


# -------------------
# Профиль
# -------------------
@user_router.get("/profile", response_class=HTMLResponse)
async def profile_page(request: Request):
    if not request.state.user:
        return RedirectResponse(url="/login", status_code=303)
    return templates.TemplateResponse("profile.html", {"request": request, "user": request.state.user})