from datetime import datetime, timezone

from sqlalchemy import BigInteger, DateTime, Integer, Numeric, SmallInteger, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database.base import Base


class VehiculoModel(Base):
    __tablename__ = "vehiculos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    condicion: Mapped[str] = mapped_column(String(10), nullable=False, default="usado")
    marca: Mapped[str] = mapped_column(String(80), nullable=False)
    modelo: Mapped[str] = mapped_column(String(100), nullable=False)
    anio: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    precio: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    kilometraje: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    transmision: Mapped[str] = mapped_column(String(15), nullable=False, default="automatica")
    combustible: Mapped[str] = mapped_column(String(15), nullable=False, default="gasolina")
    descripcion: Mapped[str] = mapped_column(Text, nullable=True)
    fotoauto: Mapped[str] = mapped_column(Text, nullable=True)
    estado: Mapped[str] = mapped_column(String(15), nullable=False, default="disponible")
    creado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=True,
    )
