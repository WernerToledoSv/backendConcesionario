from dataclasses import dataclass
from decimal import Decimal
from typing import List


@dataclass
class SolicitudesPorMesResponseDTO:
    anio: int
    mes: int
    total: int


@dataclass
class EstadisticasResponseDTO:
    vehiculos_total: int
    vehiculos_disponibles: int
    vehiculos_reservados: int
    vehiculos_vendidos: int
    solicitudes_total: int
    solicitudes_pendientes: int
    solicitudes_contactadas: int
    solicitudes_confirmadas: int
    solicitudes_rechazadas: int
    solicitudes_canceladas: int
    solicitudes_completadas: int
    solicitudes_total_estimado: Decimal
    solicitudes_confirmadas_completadas_estimado: Decimal
    solicitudes_por_mes: List[SolicitudesPorMesResponseDTO]
