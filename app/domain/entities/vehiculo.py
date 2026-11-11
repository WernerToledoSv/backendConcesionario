from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class Vehiculo:
    id: Optional[int]
    condicion: str           # 'nuevo' | 'usado'
    marca: str
    modelo: str
    anio: int
    precio: Decimal
    kilometraje: int
    transmision: str         # 'manual' | 'automatica' | 'otra'
    combustible: str         # 'gasolina' | 'diesel' | 'hibrido' | 'electrico' | 'otro'
    descripcion: Optional[str]
    fotoauto: Optional[str]  # URL de Cloudinary
    estado: str              # 'disponible' | 'reservado' | 'vendido'
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
