from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.vehiculo import Vehiculo


class VehiculoRepository(ABC):

    @abstractmethod
    def get_by_id(self, vehiculo_id: int) -> Optional[Vehiculo]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Vehiculo]:
        raise NotImplementedError

    @abstractmethod
    def save(self, vehiculo: Vehiculo) -> Vehiculo:
        raise NotImplementedError

    @abstractmethod
    def update(self, vehiculo: Vehiculo) -> Vehiculo:
        raise NotImplementedError

    @abstractmethod
    def delete(self, vehiculo_id: int) -> None:
        raise NotImplementedError
