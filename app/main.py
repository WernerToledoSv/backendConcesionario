from fastapi import FastAPI
from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.infrastructure.database.connection import engine
from app.presentation.api.v1.router import api_router

app = FastAPI(
    title="AutoMarket API",
    description="Backend del sistema de venta de vehículos AutoMarket",
    version="1.0.0",
)

app.include_router(api_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}


@app.get("/health/db", tags=["Health"])
def health_db():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"database": "ok"}
    except OperationalError:
        return {"database": "unavailable"}
