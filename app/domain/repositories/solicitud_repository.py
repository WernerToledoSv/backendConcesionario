from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.solicitud_compra import SolicitudCompra


class SolicitudRepository(ABC):
    @abstractmethod
    def get_by_id(self, solicitud_id: int) -> Optional[SolicitudCompra]:
        raise NotImplementedError

    @abstractmethod
    def create(
        self,
        nombre_cliente: str,
        correo_cliente: str,
        telefono_cliente: str,
        vehiculos_ids: List[int],
        mensaje_cliente: Optional[str] = None,
    ) -> SolicitudCompra:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[SolicitudCompra]:
        raise NotImplementedError

    @abstractmethod
    def update_notas_administrador(
        self,
        solicitud_id: int,
        notas_administrador: Optional[str],
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    def update_estado(
        self,
        solicitud_id: int,
        estado_actual: str,
        estado_nuevo: str,
    ) -> bool:
        raise NotImplementedError