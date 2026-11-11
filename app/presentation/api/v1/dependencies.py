from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.connection import get_db
from app.infrastructure.repositories.sqlalchemy_administrador_repository import (
    SQLAlchemyAdministradorRepository,
)
from app.infrastructure.security.password_hasher import PasswordHasher


def get_administrador_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SQLAlchemyAdministradorRepository:
    return SQLAlchemyAdministradorRepository(db)


def get_password_hasher() -> PasswordHasher:
    return PasswordHasher()
