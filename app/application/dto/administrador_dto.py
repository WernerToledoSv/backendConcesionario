from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CrearAdministradorDTO:
    nombre: str
    correo: str
    password: str


@dataclass
class ActualizarAdministradorDTO:
    nombre: Optional[str] = None
    correo: Optional[str] = None
    password: Optional[str] = None
    activo: Optional[bool] = None


@dataclass
class AdministradorResponseDTO:
    id: int
    nombre: str
    correo: str
    activo: bool
    creado_en: Optional[datetime]
    actualizado_en: Optional[datetime]
