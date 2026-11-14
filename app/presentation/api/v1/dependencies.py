from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import InvalidAccessTokenError
from app.domain.entities.administrador import Administrador
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
from app.infrastructure.security.jwt_service import get_admin_id_from_access_token

bearer_scheme = HTTPBearer(auto_error=False)


def get_administrador_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyAdministradorRepository:
    return SQLAlchemyAdministradorRepository(db)


def get_current_admin(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    repository: Annotated[
        SQLAlchemyAdministradorRepository,
        Depends(get_administrador_repository),
    ],
) -> Administrador:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 0, "message": "Se requiere autenticación."},
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        admin_id = get_admin_id_from_access_token(credentials.credentials)
    except InvalidAccessTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 0, "message": "El token es inválido o ha expirado."},
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    admin = repository.get_by_id(admin_id)
    if admin is None or not admin.activo:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 0, "message": "El token es inválido o ha expirado."},
            headers={"WWW-Authenticate": "Bearer"},
        )
    return admin


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
