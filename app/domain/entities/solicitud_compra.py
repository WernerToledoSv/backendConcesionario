from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from app.domain.entities.detalle_solicitud import DetalleSolicitud


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