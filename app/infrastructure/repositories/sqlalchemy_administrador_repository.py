from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.administrador import Administrador
from app.domain.repositories.administrador_repository import AdministradorRepository
from app.infrastructure.models.administrador_model import AdministradorModel


class SQLAlchemyAdministradorRepository(AdministradorRepository):
    def __init__(self, db: Session):
        self._db = db

    @staticmethod
    def _to_entity(model: AdministradorModel) -> Administrador:
        return Administrador(
            id=model.id,
            nombre=model.nombre,
            correo=model.correo,
            password_hash=model.password_hash,
            activo=model.activo,
            creado_en=model.creado_en,
            actualizado_en=model.actualizado_en,
        )

    def get_by_id(self, administrador_id: int) -> Optional[Administrador]:
        model = self._db.get(AdministradorModel, administrador_id)
        return self._to_entity(model) if model else None

    def get_by_correo(self, correo: str) -> Optional[Administrador]:
        model = (
            self._db.query(AdministradorModel)
            .filter(func.lower(AdministradorModel.correo) == correo.strip().lower())
            .first()
        )
        return self._to_entity(model) if model else None

    def get_all(self) -> List[Administrador]:
        models = self._db.query(AdministradorModel).all()
        return [self._to_entity(model) for model in models]

    def save(self, administrador: Administrador) -> Administrador:
        model = AdministradorModel(
            nombre=administrador.nombre,
            correo=administrador.correo,
            password_hash=administrador.password_hash,
            activo=administrador.activo,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, administrador: Administrador) -> Administrador:
        model = self._db.get(AdministradorModel, administrador.id)
        if model is None:
            raise LookupError("El administrador ya no existe.")
        model.nombre = administrador.nombre
        model.correo = administrador.correo
        model.password_hash = administrador.password_hash
        model.activo = administrador.activo
        model.actualizado_en = datetime.now(timezone.utc)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def delete(self, administrador_id: int) -> None:
        model = self._db.get(AdministradorModel, administrador_id)
        if model is not None:
            self._db.delete(model)
            self._db.commit()
