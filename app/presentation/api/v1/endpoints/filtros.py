from decimal import Decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, Query, status

from app.application.use_cases.vehiculos.filtrar_vehiculos import FiltrarVehiculosUseCase
from app.infrastructure.repositories.sqlalchemy_vehiculo_repository import (
    SQLAlchemyVehiculoRepository,
)
from app.presentation.api.v1.dependencies import get_vehiculo_repository
from app.presentation.api.v1.endpoints.vehiculos import _to_response
from app.presentation.api.v1.schemas.response_schema import ResponseBase, ResponseItems
from app.presentation.api.v1.schemas.vehiculo_schema import VehiculoResponse

router = APIRouter(prefix="/filtros", tags=["Filtros de vehículos"])
RepoDep = Annotated[
    SQLAlchemyVehiculoRepository,
    Depends(get_vehiculo_repository),
]


@router.get(
    "/Vehiculos",
    response_model=ResponseItems[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Buscar vehículos con filtros opcionales",
    responses={
        422: {
            "model": ResponseBase,
            "description": "Los parámetros enviados no son válidos.",
        }
    },
)
def filtrar_vehiculos(
    repo: RepoDep,
    marca: Annotated[Optional[str], Query(max_length=80)] = None,
    transmision: Annotated[Optional[str], Query(max_length=15)] = None,
    combustible: Annotated[Optional[str], Query(max_length=15)] = None,
    precio_minimo: Annotated[
        Optional[Decimal], Query(alias="precioMinimo", ge=0)
    ] = None,
    precio_maximo: Annotated[
        Optional[Decimal], Query(alias="precioMaximo", ge=0)
    ] = None,
    anio: Annotated[Optional[int], Query(ge=1900)] = None,
    condicion: Annotated[Optional[str], Query(max_length=10)] = None,
    kilometraje_minimo: Annotated[
        Optional[int], Query(alias="kilometrajeMinimo", ge=0)
    ] = None,
    kilometraje_maximo: Annotated[
        Optional[int], Query(alias="kilometrajeMaximo", ge=0)
    ] = None,
):
    items = FiltrarVehiculosUseCase(repo).execute(
        marca=marca.strip() or None if marca is not None else None,
        transmision=transmision.strip() or None if transmision is not None else None,
        combustible=combustible.strip() or None if combustible is not None else None,
        precio_minimo=precio_minimo,
        precio_maximo=precio_maximo,
        anio=anio,
        condicion=condicion.strip() or None if condicion is not None else None,
        kilometraje_minimo=kilometraje_minimo,
        kilometraje_maximo=kilometraje_maximo,
    )
    return ResponseItems(
        code=1,
        message="Vehículos filtrados exitosamente.",
        items=[_to_response(vehiculo) for vehiculo in items],
    )
