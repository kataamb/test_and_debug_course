from fastapi import HTTPException, status
from typing import Optional, List


class BaseAPIException(HTTPException):
    """Базовый класс для всех кастомных исключений"""

    def __init__(
            self,
            status_code: int,
            error: str,
            code: int,
            message: str,
            details: Optional[List[str]] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                "code": code,
                "message": message,
                "details": details or []
            }
        )


class ValidationError(BaseAPIException):
    """Ошибка валидации данных"""

    def __init__(self, message: str = "Validation failed", details: Optional[List[str]] = None):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            error="VALIDATION_ERROR",
            code=400,
            message=message,
            details=details
        )


class AuthenticationError(BaseAPIException):
    """Ошибка аутентификации"""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="AUTHENTICATION_ERROR",
            code=401,
            message=message
        )


class AuthorizationError(BaseAPIException):
    """Ошибка авторизации"""

    def __init__(self, message: str = "Access denied"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error="ACCESS_DENIED",
            code=403,
            message=message
        )


class UserNotRegisteredError(BaseAPIException):
    """Пользователь не зарегистрирован"""

    def __init__(self, message: str = "User not registered"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            error="USER_NOT_REGISTERED",
            code=401,
            message=message
        )


class InvalidCredentialsError(BaseAPIException):
    """Неверные учетные данные"""

    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            error="INVALID_CREDENTIALS",
            code=403,
            message=message
        )


class NotFoundError(BaseAPIException):
    """Ресурс не найден"""

    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            error="RESOURCE_NOT_FOUND",
            code=404,
            message=f"{resource} not found"
        )


class UserAlreadyExistsError(BaseAPIException):
    """Пользователь уже существует"""

    def __init__(self, message: str = "User already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error="USER_ALREADY_EXISTS",
            code=409,
            message=message
        )


class DatabaseError(BaseAPIException):
    """Ошибка базы данных"""

    def __init__(self, message: str = "Database error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="DATABASE_ERROR",
            code=500,
            message=message
        )


class InternalServerError(BaseAPIException):
    """Внутренняя ошибка сервера"""

    def __init__(self, message: str = "Internal server error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="INTERNAL_SERVER_ERROR",
            code=500,
            message=message
        )


class AdvertNotFoundError(NotFoundError):
    """Объявление не найдено"""

    def __init__(self):
        super().__init__("Advert")


class CategoryNotFoundError(NotFoundError):
    """Категория не найдена"""

    def __init__(self):
        super().__init__("Category")


class LikeAlreadyExistsError(BaseAPIException):
    """Лайк уже существует"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error="LIKE_ALREADY_EXISTS",
            code=409,
            message="Like already exists"
        )


class LikeNotFoundError(NotFoundError):
    """Лайк не найден"""

    def __init__(self):
        super().__init__("Like")


class DealAlreadyExistsError(BaseAPIException):
    """Сделка уже существует"""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            error="DEAL_ALREADY_EXISTS",
            code=409,
            message="Deal already exists for this advert"
        )