from datetime import datetime, timezone
from decimal import Decimal
from typing import Dict

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.domain.entities.estadisticas import Estadisticas, SolicitudesPorMes
from app.domain.repositories.estadisticas_repository import EstadisticasRepository
from app.infrastructure.models.solicitud_model import SolicitudCompraModel
from app.infrastructure.models.vehiculo_model import VehiculoModel


SOLICITUD_ESTADOS = (
    "pendiente",
    "contactado",
    "confirmada",
    "rechazada",
    "cancelada",
    "completada",
)


class SQLAlchemyEstadisticasRepository(EstadisticasRepository):
    def __init__(self, db: Session):
        self._db = db

    def get_resumen(self) -> Estadisticas:
        vehiculos_por_estado = dict(
            self._db.query(VehiculoModel.estado, func.count(VehiculoModel.id))
            .group_by(VehiculoModel.estado)
            .all()
        )
        solicitudes_rows = (
            self._db.query(
                SolicitudCompraModel.estado,
                func.count(SolicitudCompraModel.id),
                func.coalesce(func.sum(SolicitudCompraModel.total_estimado), 0),
            )
            .group_by(SolicitudCompraModel.estado)
            .all()
        )

        solicitudes_por_estado: Dict[str, int] = {
            estado: 0 for estado in SOLICITUD_ESTADOS
        }
        solicitudes_total_estimado = Decimal("0.00")
        confirmadas_completadas_estimado = Decimal("0.00")
        for estado, cantidad, total_estimado in solicitudes_rows:
            solicitudes_por_estado[estado] = cantidad
            monto = Decimal(str(total_estimado))
            solicitudes_total_estimado += monto
            if estado in ("confirmada", "completada"):
                confirmadas_completadas_estimado += monto

        meses = self._get_solicitudes_por_mes()
        return Estadisticas(
            vehiculos_total=sum(vehiculos_por_estado.values()),
            vehiculos_disponibles=vehiculos_por_estado.get("disponible", 0),
            vehiculos_reservados=vehiculos_por_estado.get("reservado", 0),
            vehiculos_vendidos=vehiculos_por_estado.get("vendido", 0),
            solicitudes_por_estado=solicitudes_por_estado,
            solicitudes_total_estimado=solicitudes_total_estimado,
            solicitudes_confirmadas_completadas_estimado=confirmadas_completadas_estimado,
            solicitudes_por_mes=meses,
        )

    def _get_solicitudes_por_mes(self) -> list[SolicitudesPorMes]:
        now = datetime.now(timezone.utc)
        current_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        month_indexes = [
            current_month.year * 12 + current_month.month - 1 - offset
            for offset in range(5, -1, -1)
        ]
        first_month = month_indexes[0]
        start = datetime(first_month // 12, first_month % 12 + 1, 1, tzinfo=timezone.utc)

        year_column = extract("year", SolicitudCompraModel.creado_en)
        month_column = extract("month", SolicitudCompraModel.creado_en)
        rows = (
            self._db.query(
                year_column.label("anio"),
                month_column.label("mes"),
                func.count(SolicitudCompraModel.id),
            )
            .filter(SolicitudCompraModel.creado_en >= start)
            .group_by(year_column, month_column)
            .all()
        )
        totals = {(int(anio), int(mes)): total for anio, mes, total in rows}
        return [
            SolicitudesPorMes(
                anio=index // 12,
                mes=index % 12 + 1,
                total=totals.get((index // 12, index % 12 + 1), 0),
            )
            for index in month_indexes
        ]
