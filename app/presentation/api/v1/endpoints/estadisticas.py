from typing import Annotated

from fastapi import APIRouter, Depends, status

from app.application.dto.estadisticas_dto import EstadisticasResponseDTO
from app.application.use_cases.estadisticas.obtener_resumen import (
    ObtenerResumenEstadisticasUseCase,
)
from app.infrastructure.repositories.sqlalchemy_estadisticas_repository import (
    SQLAlchemyEstadisticasRepository,
)
from app.presentation.api.v1.dependencies import (
    get_current_admin,
    get_estadisticas_repository,
)
from app.presentation.api.v1.schemas.estadisticas_schema import (
    EstadisticasResponse,
    SolicitudesPorMesResponse,
)
from app.presentation.api.v1.schemas.response_schema import ResponseItem

router = APIRouter(prefix="/estadisticas", tags=["Estadísticas"])
RepoDep = Annotated[
    SQLAlchemyEstadisticasRepository,
    Depends(get_estadisticas_repository),
]


def _to_response(dto: EstadisticasResponseDTO) -> EstadisticasResponse:
    return EstadisticasResponse(
        vehiculos_total=dto.vehiculos_total,
        vehiculos_disponibles=dto.vehiculos_disponibles,
        vehiculos_reservados=dto.vehiculos_reservados,
        vehiculos_vendidos=dto.vehiculos_vendidos,
        solicitudes_total=dto.solicitudes_total,
        solicitudes_pendientes=dto.solicitudes_pendientes,
        solicitudes_contactadas=dto.solicitudes_contactadas,
        solicitudes_confirmadas=dto.solicitudes_confirmadas,
        solicitudes_rechazadas=dto.solicitudes_rechazadas,
        solicitudes_canceladas=dto.solicitudes_canceladas,
        solicitudes_completadas=dto.solicitudes_completadas,
        solicitudes_total_estimado=dto.solicitudes_total_estimado,
        solicitudes_confirmadas_completadas_estimado=(
            dto.solicitudes_confirmadas_completadas_estimado
        ),
        solicitudes_por_mes=[
            SolicitudesPorMesResponse(
                anio=mes.anio,
                mes=mes.mes,
                total=mes.total,
            )
            for mes in dto.solicitudes_por_mes
        ],
    )


@router.get(
    "/Resumen",
    response_model=ResponseItem[EstadisticasResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener resumen de inventario y solicitudes",
    dependencies=[Depends(get_current_admin)],
)
def obtener_resumen_estadisticas(repo: RepoDep):
    resumen = ObtenerResumenEstadisticasUseCase(repo).execute()
    return ResponseItem(
        code=1,
        message="Estadísticas obtenidas exitosamente.",
        item=_to_response(resumen),
    )
