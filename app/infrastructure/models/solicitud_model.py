from datetime import datetime, timezone
from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import BigInteger, DateTime, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.base import Base

if TYPE_CHECKING:
    from app.infrastructure.models.detalle_solicitud_model import DetalleSolicitudModel


class SolicitudCompraModel(Base):
    __tablename__ = "solicitudes_compra"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    nombre_cliente: Mapped[str] = mapped_column(String(150), nullable=False)
    correo_cliente: Mapped[str] = mapped_column(String(180), nullable=False)
    telefono_cliente: Mapped[str] = mapped_column(String(30), nullable=False)
    estado: Mapped[str] = mapped_column(String(15), nullable=False, default="pendiente")
    total_estimado: Mapped[Decimal] = mapped_column(
        Numeric(12, 2), nullable=False, default=Decimal("0.00")
    )
    mensaje_cliente: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    notas_administrador: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    actualizado_en: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
    detalles: Mapped[List["DetalleSolicitudModel"]] = relationship(
        back_populates="solicitud",
        lazy="selectin",
    )