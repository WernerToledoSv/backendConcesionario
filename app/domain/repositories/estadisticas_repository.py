from abc import ABC, abstractmethod

from app.domain.entities.estadisticas import Estadisticas


class EstadisticasRepository(ABC):
    @abstractmethod
    def get_resumen(self) -> Estadisticas:
        raise NotImplementedError
