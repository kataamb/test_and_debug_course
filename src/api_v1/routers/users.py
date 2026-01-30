from fastapi import APIRouter, Depends, Request, status
from fastapi.security import HTTPBearer

from api_v1.dto.user_dto import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse,
    SuccessResponse
)
from service_locator import get_locator, ServiceLocator

##api_v1_users_router = APIRouter(prefix="/api/v1/users", tags=["Users"])



from core.create_jwt import get_current_user



# Добавляем security для JWT
security = HTTPBearer()


api_v1_users_router = APIRouter(
    prefix="/api/v1/users",
    tags=["Users"],

)

@api_v1_users_router.get("/debug")
async def debug_headers(request: Request):
    """Проверяем какие заголовки приходят"""
    auth_header = request.headers.get("Authorization")
    return {
        "authorization_header": auth_header,
        "all_headers": dict(request.headers),
        "has_user": hasattr(request.state, 'user'),
        "user": getattr(request.state, 'user', None)
    }

@api_v1_users_router.get("/test-simple")
async def test_simple(
    credentials = Depends(security)  # ← Прямо здесь, без своей функции
):
    return {
        "message": "Успех!",
        "token": credentials.credentials,
        "received_auth": True
    }

@api_v1_users_router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
        user_data: UserRegister,
        request: Request,
        locator: ServiceLocator = Depends(get_locator)
):
    """
    Register new user
    """
    try:
        service = locator.auth_service()

        # Преобразуем DTO в формат для твоего сервиса
        user_dict = {
            "nickname": user_data.username,
            "fio": user_data.full_name,
            "email": user_data.email,
            "phone_number": user_data.phone,
            "password": user_data.password,
            "repeat_password": user_data.rep_password  # Для совместимости с твоим сервисом
        }

        # Вызываем твой существующий сервис
        created_user = await service.register(locator.session, user_dict)

        # Временно возвращаем заглушку - нужно адаптировать твой сервис
        # чтобы он возвращал созданного пользователя
        if created_user is None:
            from api_v1.errors.errors import ValidationError
            raise ValidationError(
                message="Registration failed - user not created",
                details=["Service returned None"]
            )

        return UserResponse(
            id=created_user.id,
            username=created_user.nickname,  # используем nickname как username
            email=created_user.email,
            full_name=created_user.fio,  # используем fio как full_name
            phone=created_user.phone_number,
        )

    except Exception as e:
        from api_v1.errors.errors import ValidationError
        raise ValidationError(
            message="Registration failed",
            details=[str(e)]
        )


@api_v1_users_router.post("/login", response_model=TokenResponse, dependencies=[])
async def login_user(
        login_data: UserLogin,
        locator: ServiceLocator = Depends(get_locator)
):
    """
    User login
    """
    try:
        service = locator.auth_service()

        token = await service.login(locator.session, login_data.email, login_data.password)


        return TokenResponse(
            access_token=token,
            token_type="Bearer",
            expires_in=3600
        )

    except Exception:
        '''from api_v1.errors.errors import InvalidCredentialsError
        raise InvalidCredentialsError(
            message="Invalid credentials",
            details=[str(e)]
        )        '''
        pass


@api_v1_users_router.post("/logout", response_model=SuccessResponse)
async def logout_user(
        request: Request,
        locator: ServiceLocator = Depends(get_locator)
):
    """
    User logout
    """
    try:
        # В твоей реализации логаут происходит через удаление куки
        # Для API просто возвращаем успех
        return SuccessResponse(message="Logged out successfully")

    except Exception:
        '''from api_v1.errors.errors import DatabaseError
        raise DatabaseError(
            message="Logout failed",
            details=[str(e)]
        )   '''
        pass


@api_v1_users_router.get("/me", response_model=UserResponse, dependencies=[Depends(security)]
# ← ВСЕ эндпоинты требуют авторизации
)
async def get_current_user_profile(
    current_user: dict = Depends(get_current_user),  # ← Используй импортированную
    locator: ServiceLocator = Depends(get_locator)
):
    return UserResponse(
        id=current_user["id"],  # ← Уже UUID, не нужно преобразовывать
        username=current_user.get("email", "unknown"),  # или current_user.get("username")
        email=current_user.get("email", "unknown@example.com"),
        full_name=current_user.get("full_name", "Unknown User"),
        phone=current_user.get("phone", "")
    )




