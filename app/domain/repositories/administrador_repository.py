from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.administrador import Administrador


class AdministradorRepository(ABC):

    @abstractmethod
    def get_by_id(self, administrador_id: int) -> Optional[Administrador]:
        raise NotImplementedError

    @abstractmethod
    def get_by_correo(self, correo: str) -> Optional[Administrador]:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[Administrador]:
        raise NotImplementedError

    @abstractmethod
    def save(self, administrador: Administrador) -> Administrador:
        raise NotImplementedError

    @abstractmethod
    def update(self, administrador: Administrador) -> Administrador:
        raise NotImplementedError

    @abstractmethod
    def delete(self, administrador_id: int) -> None:
        raise NotImplementedError
