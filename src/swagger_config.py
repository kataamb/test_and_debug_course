# swagger_config.py
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi


def create_versioned_app(version: str, title: str, description: str = ""):
    """
    Создает версионированное приложение с кастомным Swagger UI
    """
    app = FastAPI(
        title=title,
        version=version,
        description=description,
        docs_url=None,  # Отключаем стандартный docs
        redoc_url=None,  # Отключаем redoc
    )

    # Кастомная Swagger UI страница
    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=f"/api/{version}/openapi.json",
            title=f"{title} - Swagger UI",
            swagger_js_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css",
        )

    # Эндпоинт для OpenAPI схемы
    @app.get("/openapi.json", include_in_schema=False)
    async def get_openapi_json():
        return get_openapi(
            title=title,
            version=version,
            description=description,
            routes=app.routes,
        )

    return app