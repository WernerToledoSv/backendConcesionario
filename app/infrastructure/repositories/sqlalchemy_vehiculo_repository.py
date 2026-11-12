from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional, Tuple, TypeVar

from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import ColumnElement

from app.domain.entities.vehiculo import Vehiculo
from app.domain.repositories.catalogo_filtro_vehiculo_repository import (
    CatalogoFiltroVehiculoRepository,
)
from app.domain.repositories.vehiculo_repository import VehiculoRepository
from app.infrastructure.models.vehiculo_model import VehiculoModel

T = TypeVar("T")


class SQLAlchemyVehiculoRepository(VehiculoRepository, CatalogoFiltroVehiculoRepository):
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

    def get_marcas(self) -> List[str]:
        return self._get_distinct_values(VehiculoModel.marca, exclude_empty=True)

    def get_transmisiones(self) -> List[str]:
        return self._get_distinct_values(VehiculoModel.transmision, exclude_empty=True)

    def get_combustibles(self) -> List[str]:
        return self._get_distinct_values(VehiculoModel.combustible, exclude_empty=True)

    def get_anios(self) -> List[int]:
        return self._get_distinct_values(VehiculoModel.anio)

    def get_condiciones(self) -> List[str]:
        return self._get_distinct_values(VehiculoModel.condicion, exclude_empty=True)

    def get_rango_precios(self) -> Tuple[Optional[Decimal], Optional[Decimal]]:
        minimo, maximo = self._db.query(
            func.min(VehiculoModel.precio),
            func.max(VehiculoModel.precio),
        ).one()
        return (
            Decimal(str(minimo)) if minimo is not None else None,
            Decimal(str(maximo)) if maximo is not None else None,
        )

    def get_rango_kilometraje(self) -> Tuple[Optional[int], Optional[int]]:
        minimo, maximo = self._db.query(
            func.min(VehiculoModel.kilometraje),
            func.max(VehiculoModel.kilometraje),
        ).one()
        return minimo, maximo

    def get_filtered(
        self,
        marca: Optional[str] = None,
        transmision: Optional[str] = None,
        combustible: Optional[str] = None,
        precio_minimo: Optional[Decimal] = None,
        precio_maximo: Optional[Decimal] = None,
        anio: Optional[int] = None,
        condicion: Optional[str] = None,
        kilometraje_minimo: Optional[int] = None,
        kilometraje_maximo: Optional[int] = None,
    ) -> List[Vehiculo]:
        query = self._db.query(VehiculoModel)
        filters = []
        if marca and marca.strip():
            filters.append(VehiculoModel.marca == marca.strip())
        if transmision and transmision.strip():
            filters.append(VehiculoModel.transmision == transmision.strip())
        if combustible and combustible.strip():
            filters.append(VehiculoModel.combustible == combustible.strip())
        if precio_minimo is not None:
            filters.append(VehiculoModel.precio >= precio_minimo)
        if precio_maximo is not None:
            filters.append(VehiculoModel.precio <= precio_maximo)
        if anio is not None:
            filters.append(VehiculoModel.anio == anio)
        if condicion and condicion.strip():
            filters.append(VehiculoModel.condicion == condicion.strip())
        if kilometraje_minimo is not None:
            filters.append(VehiculoModel.kilometraje >= kilometraje_minimo)
        if kilometraje_maximo is not None:
            filters.append(VehiculoModel.kilometraje <= kilometraje_maximo)

        models = query.filter(*filters).all()
        return [self._to_entity(model) for model in models]

    def _get_distinct_values(
        self,
        column: ColumnElement[T],
        exclude_empty: bool = False,
    ) -> List[T]:
        query = self._db.query(column).filter(column.isnot(None))
        if exclude_empty:
            query = query.filter(func.trim(column) != "")
        return [value for (value,) in query.distinct().order_by(column).all()]

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
