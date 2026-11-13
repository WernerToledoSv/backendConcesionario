from datetime import datetime
from decimal import Decimal
from typing import Annotated, List, Literal, Optional

from pydantic import BaseModel, EmailStr, Field, field_validator


class CrearSolicitudRequest(BaseModel):
    nombre_cliente: str = Field(..., min_length=2, max_length=150)
    correo_cliente: EmailStr
    telefono_cliente: str = Field(..., min_length=1, max_length=30)
    vehiculos_ids: Annotated[List[int], Field(min_length=1)]
    mensaje_cliente: Optional[str] = Field(default=None, max_length=5000)

    model_config = {"extra": "forbid"}

    @field_validator("vehiculos_ids")
    @classmethod
    def validar_vehiculos(cls, vehiculos_ids: List[int]) -> List[int]:
        if any(vehiculo_id <= 0 for vehiculo_id in vehiculos_ids):
            raise ValueError("Los identificadores de vehículos deben ser positivos.")
        if len(vehiculos_ids) != len(set(vehiculos_ids)):
            raise ValueError("No se pueden repetir vehículos en una solicitud.")
        return vehiculos_ids


class ActualizarEstadoSolicitudRequest(BaseModel):
    estado: Literal[
        "pendiente",
        "contactado",
        "confirmada",
        "rechazada",
        "cancelada",
        "completada",
    ]


class ActualizarNotasSolicitudRequest(BaseModel):
    notas_administrador: Optional[str] = Field(..., max_length=5000)


class DetalleSolicitudResponse(BaseModel):
    id: int
    vehiculo_id: int
    precio_unitario: Decimal
    marca: str
    modelo: str
    anio: int
    fotoauto: Optional[str]


class SolicitudCompraResponse(BaseModel):
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
    detalles: List[DetalleSolicitudResponse]