from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.use_cases.vehiculos.obtener_catalogos import (
    ObtenerCatalogosVehiculoUseCase,
)
from app.infrastructure.repositories.sqlalchemy_vehiculo_repository import (
    SQLAlchemyVehiculoRepository,
)
from app.presentation.api.v1.dependencies import get_vehiculo_repository
from app.presentation.api.v1.schemas.catalogosgenerales_schema import (
    RangoKilometrajeResponse,
    RangoPreciosResponse,
)
from app.presentation.api.v1.schemas.response_schema import ResponseItem, ResponseItems

router = APIRouter(prefix="/catalogosgenerales", tags=["Catálogos generales"])
RepoDep = Annotated[
    SQLAlchemyVehiculoRepository,
    Depends(get_vehiculo_repository),
]


@router.get(
    "/Marcas",
    response_model=ResponseItems[str],
    status_code=status.HTTP_200_OK,
    summary="Obtener marcas de vehículos",
)
def obtener_marcas(repo: RepoDep):
    return ResponseItems(
        code=1,
        message="Marcas obtenidas exitosamente.",
        items=ObtenerCatalogosVehiculoUseCase(repo).marcas(),
    )


@router.get(
    "/Transmisiones",
    response_model=ResponseItems[str],
    status_code=status.HTTP_200_OK,
    summary="Obtener tipos de transmisión",
)
def obtener_transmisiones(repo: RepoDep):
    return ResponseItems(
        code=1,
        message="Transmisiones obtenidas exitosamente.",
        items=ObtenerCatalogosVehiculoUseCase(repo).transmisiones(),
    )


@router.get(
    "/Combustibles",
    response_model=ResponseItems[str],
    status_code=status.HTTP_200_OK,
    summary="Obtener tipos de combustible",
)
def obtener_combustibles(repo: RepoDep):
    return ResponseItems(
        code=1,
        message="Combustibles obtenidos exitosamente.",
        items=ObtenerCatalogosVehiculoUseCase(repo).combustibles(),
    )


@router.get(
    "/RangoPrecios",
    response_model=ResponseItem[RangoPreciosResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener rango de precios",
)
def obtener_rango_precios(repo: RepoDep):
    minimo, maximo = ObtenerCatalogosVehiculoUseCase(repo).rango_precios()
    return ResponseItem(
        code=1,
        message="Rango de precios obtenido exitosamente.",
        item=RangoPreciosResponse(minimo=minimo, maximo=maximo),
    )


@router.get(
    "/Anios",
    response_model=ResponseItems[int],
    status_code=status.HTTP_200_OK,
    summary="Obtener años de fabricación",
)
def obtener_anios(repo: RepoDep):
    return ResponseItems(
        code=1,
        message="Años obtenidos exitosamente.",
        items=ObtenerCatalogosVehiculoUseCase(repo).anios(),
    )


@router.get(
    "/Condiciones",
    response_model=ResponseItems[str],
    status_code=status.HTTP_200_OK,
    summary="Obtener condiciones de vehículos",
)
def obtener_condiciones(repo: RepoDep):
    return ResponseItems(
        code=1,
        message="Condiciones obtenidas exitosamente.",
        items=ObtenerCatalogosVehiculoUseCase(repo).condiciones(),
    )


@router.get(
    "/RangoKilometraje",
    response_model=ResponseItem[RangoKilometrajeResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener rango de kilometraje",
)
def obtener_rango_kilometraje(repo: RepoDep):
    minimo, maximo = ObtenerCatalogosVehiculoUseCase(repo).rango_kilometraje()
    return ResponseItem(
        code=1,
        message="Rango de kilometraje obtenido exitosamente.",
        item=RangoKilometrajeResponse(minimo=minimo, maximo=maximo),
    )
