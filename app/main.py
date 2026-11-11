import logging

from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.infrastructure.database.connection import engine
from app.presentation.api.v1.router import api_router

logger = logging.getLogger(__name__)

# docs_url=None y redoc_url=None para deshabilitar las rutas por defecto
# y servirlas manualmente con assets locales (sin CDN)
app = FastAPI(
    title="AutoMarket API",
    description="Backend del sistema de venta de vehículos AutoMarket",
    version="1.0.0",
    docs_url=None,
    redoc_url=None,
)

app.include_router(api_router)


@app.get("/docs", include_in_schema=False)
def custom_swagger():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title="AutoMarket API - Swagger UI",
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


@app.get("/redoc", include_in_schema=False)
def custom_redoc():
    return get_redoc_html(
        openapi_url="/openapi.json",
        title="AutoMarket API - ReDoc",
        redoc_js_url="https://unpkg.com/redoc@latest/bundles/redoc.standalone.js",
    )


@app.get("/openapi.json", include_in_schema=False)
def openapi_schema():
    return get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/health/db", tags=["Health"])
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "ok"}
    except Exception as exc:
        logger.error("health/db error: %s", exc)
        return {"database": "unavailable", "detail": str(exc)}
