from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routers.deal import deals_router
from routers.main import main_router
from routers.user import user_router
#from routers.advert import advert_router
from routers.api.v1.advert import api_v1_advert_router
from routers.liked import likes_router


from core.create_jwt import JWTManager

import logging
import logging.config
import json
import os
import sys
from pathlib import Path


def setup_logging():
    config_path = os.getenv('LOG_CONFIG', 'log_config.json')

    # Проверяем доступность файла конфигурации
    if not os.path.exists(config_path):
        print(f"CRITICAL: Log config file not found: {config_path}")
        sys.exit(1)

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)

        # Проверяем доступность директории для логов
        log_dir = Path("/app/logs")
        if not log_dir.exists():
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                print(f"Created log directory: {log_dir}")
            except PermissionError as e:
                print(f"CRITICAL: Permission denied to create log directory: {log_dir}")
                print(f"Error: {e}")
                sys.exit(1)

        # Проверяем доступность файла логов для записи
        log_file = log_dir / "all_logs.log"
        try:
            # Пробуем открыть файл для записи
            with open(log_file, 'a') as f:
                f.write("")
        except PermissionError as e:
            print(f"CRITICAL: Permission denied to write to log file: {log_file}")
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"CRITICAL: Cannot access log file {log_file}: {e}")
            sys.exit(1)

        # Если все проверки прошли, настраиваем логирование
        logging.config.dictConfig(config)
        logging.info("Logging configuration loaded successfully")

    except json.JSONDecodeError as e:
        print(f"CRITICAL: Invalid JSON in log config file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"CRITICAL: Failed to load logging config: {e}")
        sys.exit(1)


# Настраиваем логирование - приложение упадет если что-то не так
setup_logging()

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Глобальный обработчик ошибок подключения к БД
@app.exception_handler(ConnectionRefusedError)
async def database_connection_exception_handler(request: Request, exc: ConnectionRefusedError) -> HTMLResponse:
    return templates.TemplateResponse(
        "database_error.html",
        {"request": request, "error": "База данных недоступна. Попробуйте позже."},
        status_code=503
    )


@app.exception_handler(Exception)
async def general_database_exception_handler(request: Request, exc: Exception) -> HTMLResponse:
    error_name = type(exc).__name__

    db_error_keywords = [
        "Connection", "Postgres", "Database", "SQL",
        "Timeout", "Operational", "Interface", "Data"
    ]

    if any(keyword in error_name for keyword in db_error_keywords):
        return templates.TemplateResponse(
            "database_error.html",
            {"request": request, "error": f"Ошибка базы данных: {error_name}"},
            status_code=503
        )
    raise exc


# Middleware: определяет текущего пользователя
@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    token = request.cookies.get("access_token")
    request.state.user = None
    if token:
        try:
            payload = JWTManager.decode_token(token)
            request.state.user = {
                "id": payload.get("id"),
                "email": payload.get("sub"),
                "role": payload.get("role"),
            }
        except Exception:
            request.state.user = None
    response = await call_next(request)
    return response

@app.on_event("startup")
async def startup_event():
    for route in app.routes:
        print(f"Path: {route.path}, Methods: {getattr(route, 'methods', None)}")


# Подключаем роутеры
#app.include_router(main_router)
#app.include_router(user_router)
#app.include_router(api_v1_advert_router)
app.include_router(api_v1_advert_router)
#app.include_router(likes_router)
#app.include_router(deals_router)

