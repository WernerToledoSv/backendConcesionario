from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field


class VehiculoResponse(BaseModel):
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

    model_config = {"from_attributes": True}


class VehiculoUpdateRequest(BaseModel):
    condicion: Optional[str] = Field(None, pattern="^(nuevo|usado)$")
    marca: Optional[str] = Field(None, max_length=80)
    modelo: Optional[str] = Field(None, max_length=100)
    anio: Optional[int] = Field(None, ge=1900)
    precio: Optional[Decimal] = Field(None, ge=0)
    kilometraje: Optional[int] = Field(None, ge=0)
    transmision: Optional[str] = Field(None, pattern="^(manual|automatica|otra)$")
    combustible: Optional[str] = Field(None, pattern="^(gasolina|diesel|hibrido|electrico|otro)$")
    descripcion: Optional[str] = None
    estado: Optional[str] = Field(None, pattern="^(disponible|reservado|vendido)$")
