from abc import ABC, abstractmethod
from typing import List

from app.domain.entities.solicitud_compra import SolicitudCompra


class SolicitudRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[SolicitudCompra]:
        raise NotImplementedError