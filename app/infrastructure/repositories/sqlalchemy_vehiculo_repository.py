from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.vehiculo import Vehiculo
from app.domain.repositories.vehiculo_repository import VehiculoRepository
from app.infrastructure.models.vehiculo_model import VehiculoModel


class SQLAlchemyVehiculoRepository(VehiculoRepository):
    def __init__(self, db: Session):
        self._db = db

    # ------------------------------------------------------------------ helpers
    @staticmethod
    def _to_entity(model: VehiculoModel) -> Vehiculo:
        return Vehiculo(
            id=model.id,
            condicion=model.condicion,
            marca=model.marca,
            modelo=model.modelo,
            anio=model.anio,
            precio=Decimal(str(model.precio)),
            kilometraje=model.kilometraje,
            transmision=model.transmision,
            combustible=model.combustible,
            descripcion=model.descripcion,
            fotoauto=model.fotoauto,
            estado=model.estado,
            creado_en=model.creado_en,
            actualizado_en=model.actualizado_en,
        )

    # ------------------------------------------------------------------ queries
    def get_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        model = self._db.get(VehiculoModel, vehiculo_id)
        return self._to_entity(model) if model else None

    def get_all(self) -> List[Vehiculo]:
        models = self._db.query(VehiculoModel).all()
        return [self._to_entity(m) for m in models]

    # ------------------------------------------------------------------ commands
    def save(self, vehiculo: Vehiculo) -> Vehiculo:
        model = VehiculoModel(
            condicion=vehiculo.condicion,
            marca=vehiculo.marca,
            modelo=vehiculo.modelo,
            anio=vehiculo.anio,
            precio=vehiculo.precio,
            kilometraje=vehiculo.kilometraje,
            transmision=vehiculo.transmision,
            combustible=vehiculo.combustible,
            descripcion=vehiculo.descripcion,
            fotoauto=vehiculo.fotoauto,
            estado=vehiculo.estado,
        )
        self._db.add(model)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def update(self, vehiculo: Vehiculo) -> Vehiculo:
        model = self._db.get(VehiculoModel, vehiculo.id)
        model.condicion = vehiculo.condicion
        model.marca = vehiculo.marca
        model.modelo = vehiculo.modelo
        model.anio = vehiculo.anio
        model.precio = vehiculo.precio
        model.kilometraje = vehiculo.kilometraje
        model.transmision = vehiculo.transmision
        model.combustible = vehiculo.combustible
        model.descripcion = vehiculo.descripcion
        model.fotoauto = vehiculo.fotoauto
        model.estado = vehiculo.estado
        model.actualizado_en = datetime.now(timezone.utc)
        self._db.commit()
        self._db.refresh(model)
        return self._to_entity(model)

    def delete(self, vehiculo_id: int) -> None:
        model = self._db.get(VehiculoModel, vehiculo_id)
        self._db.delete(model)
        self._db.commit()
