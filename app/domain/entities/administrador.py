from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Administrador:
    id: Optional[int]
    nombre: str
    correo: str
    password_hash: str
    activo: bool = True
    creado_en: Optional[datetime] = None
    actualizado_en: Optional[datetime] = None
