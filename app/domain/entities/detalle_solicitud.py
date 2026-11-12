from dataclasses import dataclass
from decimal import Decimal
from typing import Optional


@dataclass
class DetalleSolicitud:
    id: int
    vehiculo_id: int
    precio_unitario: Decimal
    marca: str
    modelo: str
    anio: int
    fotoauto: Optional[str]