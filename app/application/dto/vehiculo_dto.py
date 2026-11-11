from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional


@dataclass
class CrearVehiculoDTO:
    condicion: str
    marca: str
    modelo: str
    anio: int
    precio: Decimal
    kilometraje: int
    transmision: str
    combustible: str
    descripcion: Optional[str]
    fotoauto: Optional[str]   # URL ya subida a Cloudinary
    estado: str


@dataclass
class ActualizarVehiculoDTO:
    condicion: Optional[str] = None
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    precio: Optional[Decimal] = None
    kilometraje: Optional[int] = None
    transmision: Optional[str] = None
    combustible: Optional[str] = None
    descripcion: Optional[str] = None
    fotoauto: Optional[str] = None
    estado: Optional[str] = None


@dataclass
class VehiculoResponseDTO:
    id: int
    condicion: str
    marca: str
    modelo: str
    anio: int
    precio: Decimal
    kilometraje: int
    transmision: str
    combustible: str
    descripcion: Optional[str]
    fotoauto: Optional[str]
    estado: str
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]
