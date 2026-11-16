from datetime import datetime, timezone
from decimal import Decimal
from typing import List, Optional

from sqlalchemy import update
from sqlalchemy.orm import Session, selectinload

from app.core.exceptions import (
    VehiculosEstadoInvalidoError,
    VehiculosSolicitudNotFoundError,
)
from app.domain.entities.detalle_solicitud import DetalleSolicitud
from app.domain.entities.solicitud_compra import EstadoSolicitud, SolicitudCompra
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

    def get_all(
        self,
        estado: Optional[EstadoSolicitud] = None,
    ) -> List[SolicitudCompra]:
        query = self._db.query(SolicitudCompraModel)
        if estado is not None:
            query = query.filter(SolicitudCompraModel.estado == estado.value)
        models = (
            query
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
        if result.rowcount != 1:
            self._db.rollback()
            return False

        vehiculos_ids = [
            row[0]
            for row in self._db.query(DetalleSolicitudModel.vehiculo_id)
            .filter(DetalleSolicitudModel.solicitud_id == solicitud_id)
            .order_by(DetalleSolicitudModel.vehiculo_id)
            .all()
        ]

        if estado_nuevo in ("confirmada", "completada"):
            vehiculos = (
                self._db.query(VehiculoModel.id, VehiculoModel.estado)
                .filter(VehiculoModel.id.in_(vehiculos_ids))
                .order_by(VehiculoModel.id)
                .with_for_update()
                .all()
            )
            estados_por_id = {vehiculo_id: estado for vehiculo_id, estado in vehiculos}
            solicitudes_confirmadas = self._get_vehicles_in_other_confirmed_requests(
                solicitud_id,
                vehiculos_ids,
            )
            estado_requerido = (
                "disponible" if estado_nuevo == "confirmada" else "reservado"
            )
            vehiculos_invalidos = [
                vehiculo_id
                for vehiculo_id in vehiculos_ids
                if estados_por_id.get(vehiculo_id) != estado_requerido
                or vehiculo_id in solicitudes_confirmadas
            ]
            if vehiculos_invalidos:
                self._db.rollback()
                raise VehiculosEstadoInvalidoError(
                    vehiculos_invalidos,
                    estado_requerido,
                )

            estado_vehiculo_nuevo = (
                "reservado" if estado_nuevo == "confirmada" else "vendido"
            )
            if vehiculos_ids:
                self._db.execute(
                    update(VehiculoModel)
                    .where(VehiculoModel.id.in_(vehiculos_ids))
                    .values(
                        estado=estado_vehiculo_nuevo,
                        actualizado_en=datetime.now(timezone.utc),
                    )
                )
        elif estado_actual == "confirmada" and estado_nuevo == "cancelada":
            vehiculos = (
                self._db.query(VehiculoModel.id, VehiculoModel.estado)
                .filter(VehiculoModel.id.in_(vehiculos_ids))
                .order_by(VehiculoModel.id)
                .with_for_update()
                .all()
            )
            solicitudes_confirmadas = self._get_vehicles_in_other_confirmed_requests(
                solicitud_id,
                vehiculos_ids,
            )
            vehiculos_a_liberar = [
                vehiculo_id
                for vehiculo_id, estado in vehiculos
                if estado == "reservado"
                and vehiculo_id not in solicitudes_confirmadas
            ]
            if vehiculos_a_liberar:
                self._db.execute(
                    update(VehiculoModel)
                    .where(
                        VehiculoModel.id.in_(vehiculos_a_liberar),
                        VehiculoModel.estado == "reservado",
                    )
                    .values(
                        estado="disponible",
                        actualizado_en=datetime.now(timezone.utc),
                    )
                )

        self._db.commit()
        return True

    def _get_vehicles_in_other_confirmed_requests(
        self,
        solicitud_id: int,
        vehiculos_ids: List[int],
    ) -> set[int]:
        if not vehiculos_ids:
            return set()
        return {
            row[0]
            for row in (
                self._db.query(DetalleSolicitudModel.vehiculo_id)
                .join(
                    SolicitudCompraModel,
                    SolicitudCompraModel.id == DetalleSolicitudModel.solicitud_id,
                )
                .filter(
                    SolicitudCompraModel.id != solicitud_id,
                    SolicitudCompraModel.estado == "confirmada",
                    DetalleSolicitudModel.vehiculo_id.in_(vehiculos_ids),
                )
                .all()
            )
        }

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
