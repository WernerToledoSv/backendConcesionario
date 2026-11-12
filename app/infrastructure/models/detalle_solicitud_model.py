from decimal import Decimal
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base
from app.infrastructure.models.solicitud_model import SolicitudCompraModel
from app.infrastructure.models.vehiculo_model import VehiculoModel


class DetalleSolicitudModel(Base):
    __tablename__ = "detalle_solicitud"
    __table_args__ = (
        UniqueConstraint("solicitud_id", "vehiculo_id", name="uq_solicitud_vehiculo"),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    solicitud_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("solicitudes_compra.id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    vehiculo_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("vehiculos.id", onupdate="CASCADE", ondelete="RESTRICT"),
        nullable=False,
    )
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    solicitud: Mapped["SolicitudCompraModel"] = relationship(
        back_populates="detalles",
    )
    vehiculo: Mapped["VehiculoModel"] = relationship(lazy="joined")