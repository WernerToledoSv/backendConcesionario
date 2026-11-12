from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, List


@dataclass
class SolicitudesPorMes:
    anio: int
    mes: int
    total: int


@dataclass
class Estadisticas:
    vehiculos_total: int
    vehiculos_disponibles: int
    vehiculos_reservados: int
    vehiculos_vendidos: int
    solicitudes_por_estado: Dict[str, int]
    solicitudes_total_estimado: Decimal
    solicitudes_confirmadas_completadas_estimado: Decimal
    solicitudes_por_mes: List[SolicitudesPorMes]
