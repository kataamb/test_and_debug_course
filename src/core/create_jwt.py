import jwt
from datetime import datetime, timedelta
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from uuid import UUID
from typing import Optional

SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class JWTManager:
    @staticmethod
    def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    @staticmethod
    def decode_token(token: str) -> dict[str, Any]:
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except jwt.PyJWTError:
            raise ValueError("Invalid token")


##########################################################################################

# файл: routes/api_v1/advert_routes.py




# Добавляем security для JWT
security = HTTPBearer()

not_strict_security = HTTPBearer(auto_error=False)


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Зависимость для получения текущего пользователя из JWT"""
    try:
        payload = JWTManager.decode_token(credentials.credentials)
        user_id = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
        return {
            "id": UUID(user_id),  # Преобразуем строку в UUID
            "email": payload.get("sub"),
            "role": payload.get("role")
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )


async def get_optional_user(
        credentials: Optional[HTTPAuthorizationCredentials] = Depends(not_strict_security)
) -> Optional[dict]:
    """Опциональная зависимость для получения текущего пользователя"""
    if not credentials:
        return None  # Не авторизован - возвращаем None

    try:
        payload = JWTManager.decode_token(credentials.credentials)
        user_id = payload.get("id")
        if user_id is None:
            return None  # Невалидный токен - считаем не авторизованным

        return {
            "id": UUID(user_id),
            "email": payload.get("sub"),
            "role": payload.get("role")
        }
    except Exception:
        return None  # Любая ошибка - считаем не авторизованным