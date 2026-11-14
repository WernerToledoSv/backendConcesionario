from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.solicitud_dto import (
    CrearSolicitudDTO,
    SolicitudCompraResponseDTO,
)
from app.application.use_cases.solicitudes.actualizar_estado import (
    ActualizarEstadoSolicitudUseCase,
)
from app.application.use_cases.solicitudes.actualizar_notas import (
    ActualizarNotasSolicitudUseCase,
)
from app.application.use_cases.solicitudes.crear_solicitud import (
    CrearSolicitudUseCase,
)
from app.application.use_cases.solicitudes.listar_solicitudes import (
    ListarSolicitudesUseCase,
)
from app.core.exceptions import (
    ConcurrentSolicitudUpdateError,
    DuplicateVehiclesInSolicitudError,
    InvalidSolicitudStateError,
    InvalidSolicitudTransitionError,
    SolicitudNotFoundError,
    VehiculosSolicitudNotFoundError,
    VehiclesNotProvidedError,
)
from app.domain.entities.solicitud_compra import SolicitudCompra
from app.infrastructure.repositories.sqlalchemy_solicitud_repository import (
    SQLAlchemySolicitudRepository,
)
from app.presentation.api.v1.dependencies import (
    get_current_admin,
    get_solicitud_repository,
)
from app.presentation.api.v1.schemas.response_schema import (
    ResponseBase,
    ResponseItem,
    ResponseItems,
)
from app.presentation.api.v1.schemas.solicitud_schema import (
    ActualizarEstadoSolicitudRequest,
    ActualizarNotasSolicitudRequest,
    CrearSolicitudRequest,
    DetalleSolicitudResponse,
    SolicitudCompraResponse,
)

router = APIRouter(prefix="/solicitudes", tags=["Solicitudes de compra"])
RepoDep = Annotated[
    SQLAlchemySolicitudRepository,
    Depends(get_solicitud_repository),
]


def _to_response(
    solicitud: SolicitudCompra | SolicitudCompraResponseDTO,
) -> SolicitudCompraResponse:
    return SolicitudCompraResponse(
        id=solicitud.id,
        nombre_cliente=solicitud.nombre_cliente,
        correo_cliente=solicitud.correo_cliente,
        telefono_cliente=solicitud.telefono_cliente,
        estado=solicitud.estado,
        total_estimado=solicitud.total_estimado,
        mensaje_cliente=solicitud.mensaje_cliente,
        notas_administrador=solicitud.notas_administrador,
        creado_en=solicitud.creado_en,
        actualizado_en=solicitud.actualizado_en,
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
            for detalle in solicitud.detalles
        ],
    )


@router.post(
    "/CrearSolicitud",
    response_model=ResponseItem[SolicitudCompraResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear una solicitud de compra",
)
def crear_solicitud(body: CrearSolicitudRequest, repo: RepoDep):
    dto = CrearSolicitudDTO(
        nombre_cliente=body.nombre_cliente,
        correo_cliente=str(body.correo_cliente),
        telefono_cliente=body.telefono_cliente,
        vehiculos_ids=body.vehiculos_ids,
        mensaje_cliente=body.mensaje_cliente,
    )
    try:
        solicitud = CrearSolicitudUseCase(repo).execute(dto)
    except (DuplicateVehiclesInSolicitudError, VehiclesNotProvidedError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "code": 0,
                "message": str(exc) or "La solicitud no tiene vehículos válidos.",
            },
        ) from exc
    except VehiculosSolicitudNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc

    return ResponseItem(
        code=1,
        message="Solicitud creada exitosamente.",
        item=_to_response(solicitud),
    )


@router.get(
    "/ListarSolicitudes",
    response_model=ResponseItems[SolicitudCompraResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar solicitudes de compra",
    dependencies=[Depends(get_current_admin)],
)
def listar_solicitudes(repo: RepoDep):
    items = ListarSolicitudesUseCase(repo).execute()
    return ResponseItems(
        code=1,
        message="Solicitudes obtenidas exitosamente.",
        items=[_to_response(solicitud) for solicitud in items],
    )


@router.patch(
    "/ActualizarNotas/{solicitud_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Actualizar las notas administrativas de una solicitud",
    dependencies=[Depends(get_current_admin)],
)
def actualizar_notas(
    solicitud_id: int,
    body: ActualizarNotasSolicitudRequest,
    repo: RepoDep,
):
    try:
        ActualizarNotasSolicitudUseCase(repo).execute(
            solicitud_id,
            body.notas_administrador,
        )
    except SolicitudNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    return ResponseBase(
        code=1,
        message="Notas de la solicitud actualizadas exitosamente.",
    )


@router.patch(
    "/ActualizarEstado/{solicitud_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Cambiar el estado de una solicitud",
    dependencies=[Depends(get_current_admin)],
)
def actualizar_estado(
    solicitud_id: int,
    body: ActualizarEstadoSolicitudRequest,
    repo: RepoDep,
):
    try:
        ActualizarEstadoSolicitudUseCase(repo).execute(solicitud_id, body.estado)
    except SolicitudNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    except InvalidSolicitudStateError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    except InvalidSolicitudTransitionError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    except ConcurrentSolicitudUpdateError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "code": 0,
                "message": "La solicitud cambió durante la actualización; vuelva a intentarlo.",
            },
        ) from exc
    return ResponseBase(
        code=1,
        message="Estado de la solicitud actualizado exitosamente.",
    )
