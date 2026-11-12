from app.application.dto.estadisticas_dto import (
    EstadisticasResponseDTO,
    SolicitudesPorMesResponseDTO,
)
from app.domain.repositories.estadisticas_repository import EstadisticasRepository


class ObtenerResumenEstadisticasUseCase:
    def __init__(self, repository: EstadisticasRepository):
        self._repository = repository

    def execute(self) -> EstadisticasResponseDTO:
        estadisticas = self._repository.get_resumen()
        solicitudes = estadisticas.solicitudes_por_estado
        return EstadisticasResponseDTO(
            vehiculos_total=estadisticas.vehiculos_total,
            vehiculos_disponibles=estadisticas.vehiculos_disponibles,
            vehiculos_reservados=estadisticas.vehiculos_reservados,
            vehiculos_vendidos=estadisticas.vehiculos_vendidos,
            solicitudes_total=sum(solicitudes.values()),
            solicitudes_pendientes=solicitudes.get("pendiente", 0),
            solicitudes_contactadas=solicitudes.get("contactado", 0),
            solicitudes_confirmadas=solicitudes.get("confirmada", 0),
            solicitudes_rechazadas=solicitudes.get("rechazada", 0),
            solicitudes_canceladas=solicitudes.get("cancelada", 0),
            solicitudes_completadas=solicitudes.get("completada", 0),
            solicitudes_total_estimado=estadisticas.solicitudes_total_estimado,
            solicitudes_confirmadas_completadas_estimado=(
                estadisticas.solicitudes_confirmadas_completadas_estimado
            ),
            solicitudes_por_mes=[
                SolicitudesPorMesResponseDTO(
                    anio=mes.anio,
                    mes=mes.mes,
                    total=mes.total,
                )
                for mes in estadisticas.solicitudes_por_mes
            ],
        )
