from abc import ABC, abstractmethod
from decimal import Decimal
from typing import List, Optional, Tuple

from app.domain.entities.vehiculo import Vehiculo


class CatalogoFiltroVehiculoRepository(ABC):
    @abstractmethod
    def get_marcas(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_transmisiones(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_combustibles(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_rango_precios(self) -> Tuple[Optional[Decimal], Optional[Decimal]]:
        raise NotImplementedError

    @abstractmethod
    def get_anios(self) -> List[int]:
        raise NotImplementedError

    @abstractmethod
    def get_condiciones(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_rango_kilometraje(self) -> Tuple[Optional[int], Optional[int]]:
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError
