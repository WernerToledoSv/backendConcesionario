from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlalchemy_administrador_repository import (
    SQLAlchemyAdministradorRepository,
)
from app.infrastructure.repositories.sqlalchemy_vehiculo_repository import (
    SQLAlchemyVehiculoRepository,
)
from app.infrastructure.repositories.sqlalchemy_solicitud_repository import (
    SQLAlchemySolicitudRepository,
)
from app.infrastructure.repositories.sqlalchemy_estadisticas_repository import (
    SQLAlchemyEstadisticasRepository,
)
from app.infrastructure.cloudinary.cloudinary_service import CloudinaryService


def get_administrador_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyAdministradorRepository:
    return SQLAlchemyAdministradorRepository(db)


def get_vehiculo_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyVehiculoRepository:
    return SQLAlchemyVehiculoRepository(db)


def get_solicitud_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemySolicitudRepository:
    return SQLAlchemySolicitudRepository(db)


def get_estadisticas_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyEstadisticasRepository:
    return SQLAlchemyEstadisticasRepository(db)


def get_cloudinary_service() -> CloudinaryService:
    return CloudinaryService()
