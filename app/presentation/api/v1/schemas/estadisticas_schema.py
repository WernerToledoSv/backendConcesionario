from decimal import Decimal
from typing import List

from pydantic import BaseModel


class SolicitudesPorMesResponse(BaseModel):
    anio: int
    mes: int
    total: int


class EstadisticasResponse(BaseModel):
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
    solicitudes_por_mes: List[SolicitudesPorMesResponse]
