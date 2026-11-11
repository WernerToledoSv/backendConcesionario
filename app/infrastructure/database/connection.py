import logging
from typing import Generator

from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

# Controla SSL en DATABASE_URL: sslmode=disable para PostgreSQL local y
# sslmode=require para Neon.
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,    # Verifica la conexión antes de usarla (esencial para Neon)
    pool_recycle=300,      # Recicla conexiones cada 5 min (Neon cierra las inactivas)
    pool_timeout=30,       # Espera hasta 30s para obtener una conexión del pool
    pool_size=5,           # Conexiones simultáneas en el pool
    max_overflow=10,       # Conexiones extra permitidas sobre pool_size
    connect_args={
        "connect_timeout": 10,       # Neon puede tardar en despertar (cold start)
        "options": "-c timezone=UTC" # Zona horaria consistente
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
