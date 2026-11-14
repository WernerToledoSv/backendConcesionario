from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import List, Optional

from app.domain.entities.detalle_solicitud import DetalleSolicitud


class EstadoSolicitud(str, Enum):
    PENDIENTE = "pendiente"
    CONTACTADO = "contactado"
    CONFIRMADA = "confirmada"
    RECHAZADA = "rechazada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"


SOLICITUD_ESTADOS = tuple(estado.value for estado in EstadoSolicitud)

TRANSICIONES_SOLICITUD = {
    "pendiente": {"contactado", "rechazada", "cancelada"},
    "contactado": {"confirmada", "rechazada", "cancelada"},
    "confirmada": {"completada", "cancelada"},
    "rechazada": set(),
    "cancelada": set(),
    "completada": set(),
}


@dataclass
class SolicitudCompra:
    id: int
    nombre_cliente: str
    correo_cliente: str
    telefono_cliente: str
    estado: str
    total_estimado: Decimal
    mensaje_cliente: Optional[str]
    notas_administrador: Optional[str]
    creado_en: datetime
    actualizado_en: Optional[datetime]
    detalles: List[DetalleSolicitud] = field(default_factory=list)