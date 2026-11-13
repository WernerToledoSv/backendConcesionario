from datetime import datetime
from typing import Optional

from pydantic import AliasChoices, BaseModel, EmailStr, Field


class AdministradorCreateRequest(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=120, examples=["Juan Pérez"])
    correo: EmailStr = Field(..., examples=["juan@automarket.com"])
    password: str = Field(..., min_length=12, max_length=128)


class AdministradorUpdateRequest(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2, max_length=120)
    correo: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=12, max_length=128)
    activo: Optional[bool] = None


class AdministradorLoginRequest(BaseModel):
    correo: EmailStr = Field(examples=["juan@automarket.com"])
    password: str = Field(
        min_length=1,
        max_length=128,
        validation_alias=AliasChoices("password", "pass"),
    )


class AdministradorResponse(BaseModel):
    id: int
    nombre: str
    correo: EmailStr
    activo: bool
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]

    model_config = {"from_attributes": True}


class LoginResponse(BaseModel):
    code: int
    message: str
    item: AdministradorResponse
    access_token: str
    token_type: str
    expires_in: int
