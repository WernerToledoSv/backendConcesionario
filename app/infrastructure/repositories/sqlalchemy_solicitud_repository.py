from decimal import Decimal
from typing import List

from sqlalchemy.orm import Session, selectinload

from app.domain.entities.detalle_solicitud import DetalleSolicitud
from app.domain.entities.solicitud_compra import SolicitudCompra
from app.domain.repositories.solicitud_repository import SolicitudRepository
from app.infrastructure.models.detalle_solicitud_model import DetalleSolicitudModel
from app.infrastructure.models.solicitud_model import SolicitudCompraModel


class SQLAlchemySolicitudRepository(SolicitudRepository):
    def __init__(self, db: Session):
        self._db = db

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