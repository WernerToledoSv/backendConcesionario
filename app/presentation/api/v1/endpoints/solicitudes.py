from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.dto.solicitud_dto import (
    DetalleSolicitudResponseDTO,
    SolicitudCompraResponseDTO,
)
from app.application.use_cases.solicitudes.listar_solicitudes import ListarSolicitudesUseCase
from app.infrastructure.repositories.sqlalchemy_solicitud_repository import (
    SQLAlchemySolicitudRepository,
)
from app.presentation.api.v1.dependencies import get_solicitud_repository
from app.presentation.api.v1.schemas.response_schema import ResponseItems
from app.presentation.api.v1.schemas.solicitud_schema import (
    DetalleSolicitudResponse,
    SolicitudCompraResponse,
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes de compra"])
RepoDep = Annotated[
    SQLAlchemySolicitudRepository,
    Depends(get_solicitud_repository),
]


def _to_response(dto: SolicitudCompraResponseDTO) -> SolicitudCompraResponse:
    return SolicitudCompraResponse(
        id=dto.id,
        nombre_cliente=dto.nombre_cliente,
        correo_cliente=dto.correo_cliente,
        telefono_cliente=dto.telefono_cliente,
        estado=dto.estado,
        total_estimado=dto.total_estimado,
        mensaje_cliente=dto.mensaje_cliente,
        notas_administrador=dto.notas_administrador,
        creado_en=dto.creado_en,
        actualizado_en=dto.actualizado_en,
        detalles=[
            DetalleSolicitudResponse(
                id=detalle.id,
                vehiculo_id=detalle.vehiculo_id,
                precio_unitario=detalle.precio_unitario,
                marca=detalle.marca,
                modelo=detalle.modelo,
                anio=detalle.anio,
                fotoauto=detalle.fotoauto,
            )
            for detalle in dto.detalles
        ],
    )


@router.get(
    "/ListarSolicitudes",
    response_model=ResponseItems[SolicitudCompraResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar solicitudes de compra",
)
def listar_solicitudes(repo: RepoDep):
    items = ListarSolicitudesUseCase(repo).execute()
    return ResponseItems(
        code=1,
        message="Solicitudes obtenidas exitosamente.",
        items=[_to_response(solicitud) for solicitud in items],
    )