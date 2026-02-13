from __future__ import annotations

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

from routers.deal import deals_router
from routers.main import main_router
from routers.user import user_router
from routers.advert import advert_router
from routers.liked import likes_router

from api_v1.routers.adverts import api_v1_adverts_router
from api_v1.routers.categories import api_v1_categories_router
from api_v1.routers.users import api_v1_users_router
from api_v1.routers.likes import api_v1_likes_router
from api_v1.routers.deals import api_v1_deals_router

from api_v2.routers.adverts import api_v2_router_adverts
from api_v2.routers.categories import api_v2_router_categories

from core.create_jwt import JWTManager

import logging
import logging.config
import json
import os
import sys
from pathlib import Path


from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

# ----------------- Logging -----------------
def setup_logging():
    config_path = os.getenv('LOG_CONFIG', 'log_config.json')
    if not os.path.exists(config_path):
        print(f"CRITICAL: Log config file not found: {config_path}")
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    log_dir = Path("/app/logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "all_logs.log"
    log_file.touch(exist_ok=True)

    logging.config.dictConfig(config)
    logging.info("Logging configuration loaded successfully")

setup_logging()

# ----------------- App -----------------
app = FastAPI(root_path="/api/v1") #root_path="/api/v1")
templates = Jinja2Templates(directory="templates")

# ----------------- CORS -----------------
app.add_middleware(
    CORSMiddleware,
    #allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "https://a69f5b5f1fa9d9c0cb2403b3847632f7.serveousercontent.com"],
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- JWT Middleware -----------------
@app.middleware("http")
async def add_user_to_request(request: Request, call_next):
    """
    Определяем текущего пользователя из access_token (JWT) и кладем в request.state.user.
    Preflight-запросы (OPTIONS) пропускаются автоматически через CORSMiddleware.
    """
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

# ----------------- Exception Handlers -----------------
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
    db_error_keywords = ["Connection", "Postgres", "Database", "SQL", "Timeout", "Operational", "Interface", "Data"]
    if any(keyword in error_name for keyword in db_error_keywords):
        return templates.TemplateResponse(
            "database_error.html",
            {"request": request, "error": f"Ошибка базы данных: {error_name}"},
            status_code=503
        )
    raise exc

# ----------------- Startup -----------------
@app.on_event("startup")
async def startup_event():
    for route in app.routes:
        print(f"Path: {route.path}, Methods: {getattr(route, 'methods', None)}")

# ----------------- Routers -----------------
app.include_router(main_router)
app.include_router(user_router)
app.include_router(advert_router)
app.include_router(likes_router)
app.include_router(deals_router)

app.include_router(api_v1_adverts_router)
app.include_router(api_v1_categories_router)
app.include_router(api_v1_users_router)
app.include_router(api_v1_likes_router)
app.include_router(api_v1_deals_router)

app.include_router(
    api_v2_router_adverts,
    prefix="/api/v2"
)

app.include_router(
    api_v2_router_categories,
    prefix="/api/v2"
)

# ----------------- Swagger -----------------


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
    filtered_paths = {path: methods for path, methods in openapi_schema["paths"].items() if path.startswith("/api/v0_1")}
    openapi_schema["paths"] = filtered_paths
    return openapi_schema

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
    filtered_paths = {path: methods for path, methods in openapi_schema["paths"].items() if path.startswith("/api/v1/")}
    openapi_schema["paths"] = filtered_paths
    return openapi_schema

