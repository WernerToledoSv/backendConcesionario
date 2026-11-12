from fastapi import APIRouter

from app.presentation.api.v1.endpoints.administradores import router as administradores_router
from app.presentation.api.v1.endpoints.catalogosgenerales import (
    router as catalogosgenerales_router,
)
from app.presentation.api.v1.endpoints.estadisticas import router as estadisticas_router
from app.presentation.api.v1.endpoints.filtros import router as filtros_router
from app.presentation.api.v1.endpoints.solicitudes import router as solicitudes_router
from app.presentation.api.v1.endpoints.vehiculos import router as vehiculos_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(administradores_router)
api_router.include_router(catalogosgenerales_router)
api_router.include_router(estadisticas_router)
api_router.include_router(filtros_router)
api_router.include_router(solicitudes_router)
api_router.include_router(vehiculos_router)
