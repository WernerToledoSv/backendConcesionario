import logging
from typing import Generator

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,       # Verifica la conexión antes de usarla
    connect_args={
        "connect_timeout": 5  # Falla rápido si la BD no responde (segundos)
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependencia de FastAPI que provee una sesión de base de datos.
    Si la BD no está disponible, retorna HTTP 503 en lugar de un error 500 genérico.
    """
    db = SessionLocal()
    try:
        yield db
    except OperationalError as exc:
        logger.error("Error de conexión con la base de datos: %s", exc)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Base de datos no disponible. Intente más tarde.",
        )
    finally:
        db.close()
