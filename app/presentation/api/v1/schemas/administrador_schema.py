from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class AdministradorCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120, examples=["Juan Pérez"])
    correo: EmailStr = Field(..., examples=["juan@automarket.com"])
    password: str = Field(..., min_length=8, examples=["segura1234"])


class AdministradorUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=120)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8)
    activo: Optional[bool] = None


class AdministradorResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    activo: bool
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}
