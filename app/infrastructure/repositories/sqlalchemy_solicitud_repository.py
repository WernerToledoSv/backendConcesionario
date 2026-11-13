from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import VehiculosSolicitudNotFoundError
from app.domain.entities.detalle_solicitud import DetalleSolicitud
from app.domain.entities.solicitud_compra import SolicitudCompra
from app.domain.repositories.solicitud_repository import SolicitudRepository
from app.infrastructure.models.detalle_solicitud_model import DetalleSolicitudModel
from app.infrastructure.models.solicitud_model import SolicitudCompraModel
from app.infrastructure.models.vehiculo_model import VehiculoModel


class SQLAlchemySolicitudRepository(SolicitudRepository):
    def __init__(self, db: Session):
        self._db = db

    def create(
        self,
        nombre_cliente: str,
        correo_cliente: str,
        telefono_cliente: str,
        vehiculos_ids: List[int],
        mensaje_cliente: Optional[str] = None,
    ) -> SolicitudCompra:
        vehiculos = (
            self._db.query(VehiculoModel)
            .filter(VehiculoModel.id.in_(vehiculos_ids))
            .order_by(VehiculoModel.id)
            .with_for_update()
            .all()
        )
        vehiculos_por_id = {vehiculo.id: vehiculo for vehiculo in vehiculos}
        faltantes = [vehiculo_id for vehiculo_id in vehiculos_ids if vehiculo_id not in vehiculos_por_id]
        if faltantes:
            self._db.rollback()
            raise VehiculosSolicitudNotFoundError(faltantes)

        detalles = [
            DetalleSolicitudModel(
                vehiculo_id=vehiculo_id,
                precio_unitario=Decimal(str(vehiculos_por_id[vehiculo_id].precio)),
                vehiculo=vehiculos_por_id[vehiculo_id],
            )
            for vehiculo_id in vehiculos_ids
        ]
        total_estimado = sum(
            (detalle.precio_unitario for detalle in detalles),
            Decimal("0.00"),
        )
        solicitud_model = SolicitudCompraModel(
            nombre_cliente=nombre_cliente,
            correo_cliente=correo_cliente,
            telefono_cliente=telefono_cliente,
            estado="pendiente",
            total_estimado=total_estimado,
            mensaje_cliente=mensaje_cliente,
            detalles=detalles,
        )
        self._db.add(solicitud_model)
        try:
            self._db.commit()
            self._db.refresh(solicitud_model)
        except Exception:
            self._db.rollback()
            raise
        return self._to_entity(solicitud_model)

    def get_by_id(self, solicitud_id: int) -> Optional[SolicitudCompra]:
        model = (
            self._db.query(SolicitudCompraModel)
            .options(
                selectinload(SolicitudCompraModel.detalles).joinedload(
                    DetalleSolicitudModel.vehiculo
                )
            )
            .filter(SolicitudCompraModel.id == solicitud_id)
            .first()
        )
        return self._to_entity(model) if model else None

    def get_all(self) -> List[SolicitudCompra]:
        models = (
            self._db.query(SolicitudCompraModel)
            .options(
                selectinload(SolicitudCompraModel.detalles).joinedload(
                    DetalleSolicitudModel.vehiculo
                )
            )
            .order_by(SolicitudCompraModel.creado_en.desc(), SolicitudCompraModel.id.desc())
            .all()
        )
        return [self._to_entity(model) for model in models]

    def update_notas_administrador(
        self,
        solicitud_id: int,
        notas_administrador: Optional[str],
    ) -> bool:
        result = self._db.execute(
            update(SolicitudCompraModel)
            .where(SolicitudCompraModel.id == solicitud_id)
            .values(
                notas_administrador=notas_administrador,
                actualizado_en=datetime.now(timezone.utc),
            )
        )
        self._db.commit()
        return result.rowcount == 1

    def update_estado(
        self,
        solicitud_id: int,
        estado_actual: str,
        estado_nuevo: str,
    ) -> bool:
        result = self._db.execute(
            update(SolicitudCompraModel)
            .where(
                SolicitudCompraModel.id == solicitud_id,
                SolicitudCompraModel.estado == estado_actual,
            )
            .values(
                estado=estado_nuevo,
                actualizado_en=datetime.now(timezone.utc),
            )
        )
        self._db.commit()
        return result.rowcount == 1

    @staticmethod
    def _to_entity(model: SolicitudCompraModel) -> SolicitudCompra:
        return SolicitudCompra(
            id=model.id,
            nombre_cliente=model.nombre_cliente,
            correo_cliente=model.correo_cliente,
            telefono_cliente=model.telefono_cliente,
            estado=model.estado,
            total_estimado=Decimal(str(model.total_estimado)),
            mensaje_cliente=model.mensaje_cliente,
            notas_administrador=model.notas_administrador,
            creado_en=model.creado_en,
            actualizado_en=model.actualizado_en,
            detalles=[
                DetalleSolicitud(
                    id=detalle.id,
                    vehiculo_id=detalle.vehiculo_id,
                    precio_unitario=Decimal(str(detalle.precio_unitario)),
                    marca=detalle.vehiculo.marca,
                    modelo=detalle.vehiculo.modelo,
                    anio=detalle.vehiculo.anio,
                    fotoauto=detalle.vehiculo.fotoauto,
                )
                for detalle in model.detalles
            ],
        )
