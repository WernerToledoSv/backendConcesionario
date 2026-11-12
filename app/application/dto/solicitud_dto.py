from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import List, Optional


@dataclass
class DetalleSolicitudResponseDTO:
    id: int
    vehiculo_id: int
    precio_unitario: Decimal
    marca: str
    modelo: str
    anio: int
    fotoauto: Optional[str]


@dataclass
class SolicitudCompraResponseDTO:
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
    detalles: List[DetalleSolicitudResponseDTO]