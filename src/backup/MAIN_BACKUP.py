from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from routers.deal import deals_router
from routers.main import main_router
from routers.user import user_router
from routers.advert import advert_router
from routers.liked import likes_router

##from fastapi.openapi.utils import get_openapi

from api_v1.routers.adverts import api_v1_adverts_router
from api_v1.routers.categories import api_v1_categories_router
from api_v1.routers.users import api_v1_users_router
from api_v1.routers.likes import api_v1_likes_router
from api_v1.routers.deals import api_v1_deals_router

from core.create_jwt import JWTManager

import logging
import logging.config
import json
import os
import sys
from pathlib import Path
import yaml

from fastapi.middleware.cors import CORSMiddleware



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

'''
@app.middleware("http")
async def add_cors_header(request: Request, call_next):
    if request.method == "OPTIONS":
        response = JSONResponse(content={"message": "OK"})
    else:
        response = await call_next(request)
    
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:5173"
    response.headers["Access-Control-Allow-Credentials"] = "true"
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "*"
    return response
'''

# 2. Потом уже стандартный CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
app.include_router(main_router)
app.include_router(user_router)
app.include_router(advert_router)

app.include_router(likes_router)
app.include_router(deals_router)

##app.include_router(api_v1_advert_router)

app.include_router(api_v1_adverts_router )
app.include_router(api_v1_categories_router )
app.include_router(api_v1_users_router )
app.include_router(api_v1_likes_router)
app.include_router(api_v1_deals_router)













####################################3


from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


# Swagger для API v0 (только multipage/legacy роуты)
@app.get("/api/v0_1/docs", include_in_schema=False)
async def v0_swagger():
    return get_swagger_ui_html(
        openapi_url="/v0-openapi.json",
        title="Legacy API v0 - Swagger UI",
    )


@app.get("/v0-openapi.json", include_in_schema=False)
async def v0_openapi():
    openapi_schema = get_openapi(
        title="Legacy API v0",
        version="0.1.0",
        description="Legacy multipage endpoints",
        routes=app.routes,
    )

    # Фильтруем - оставляем только multipage роуты
    filtered_paths = {}
    for path, methods in openapi_schema["paths"].items():
        # Показываем multipage роуты (исключаем /api/ пути)
        if path.startswith("/api/v0_1"):
            filtered_paths[path] = methods

    openapi_schema["paths"] = filtered_paths
    return openapi_schema


# Swagger для API v1 (только REST API)
@app.get("/api/v1/docs", include_in_schema=False)
async def v1_swagger():
    return get_swagger_ui_html(
        openapi_url="/v1-openapi.json",
        title="REST API v1 - Swagger UI",
    )


@app.get("/v1-openapi.json", include_in_schema=False)
async def v1_openapi():
    openapi_schema = get_openapi(
        title="REST API v1",
        version="1.0.0",
        description="REST API endpoints",
        routes=app.routes,
    )

    # Фильтруем - оставляем только API v1 роуты
    filtered_paths = {}
    for path, methods in openapi_schema["paths"].items():
        # Показываем только /api/v1/ пути
        if path.startswith("/api/v1/"):
            filtered_paths[path] = methods

    openapi_schema["paths"] = filtered_paths
    return openapi_schema


