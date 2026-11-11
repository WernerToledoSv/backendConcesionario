from fastapi import APIRouter

from app.presentation.api.v1.endpoints.administradores import router as administradores_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(administradores_router)
