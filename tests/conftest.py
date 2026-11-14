import os

import pytest
from sqlalchemy import BigInteger, create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["DATABASE_URL"] = "postgresql+psycopg2://test:test@localhost/test"
os.environ["JWT_SECRET_KEY"] = "test-only-signing-key-not-used-in-production-1234"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "15"
os.environ["JWT_ISSUER"] = "automarket-api-test"
os.environ["CLOUDINARY_CLOUD_NAME"] = "test"
os.environ["CLOUDINARY_API_KEY"] = "test"
os.environ["CLOUDINARY_API_SECRET"] = "test"


@compiles(BigInteger, "sqlite")
def compile_big_integer_for_sqlite(_type, _compiler, **_kwargs):
    return "INTEGER"


from app.infrastructure.database.base import Base
from app.infrastructure.database.connection import get_db
from app.infrastructure.models.administrador_model import AdministradorModel
from app.infrastructure.models.detalle_solicitud_model import DetalleSolicitudModel
from app.infrastructure.models.solicitud_model import SolicitudCompraModel
from app.infrastructure.models.vehiculo_model import VehiculoModel
from app.main import app


def make_test_session_factory():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine, expire_on_commit=False)


@pytest.fixture
def test_db():
    engine, session_factory = make_test_session_factory()
    yield session_factory
    Base.metadata.drop_all(engine)
    engine.dispose()


@pytest.fixture
def client(test_db):
    from fastapi.testclient import TestClient

    def override_get_db():
        with test_db() as db:
            yield db

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
