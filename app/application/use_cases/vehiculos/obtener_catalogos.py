from decimal import Decimal
from typing import List, Optional, Tuple

from app.domain.repositories.catalogo_filtro_vehiculo_repository import (
    CatalogoFiltroVehiculoRepository,
)


class ObtenerCatalogosVehiculoUseCase:
    def __init__(self, repository: CatalogoFiltroVehiculoRepository):
        self._repository = repository

    def marcas(self) -> List[str]:
        return self._repository.get_marcas()

    def transmisiones(self) -> List[str]:
        return self._repository.get_transmisiones()

    def combustibles(self) -> List[str]:
        return self._repository.get_combustibles()

    def rango_precios(self) -> Tuple[Optional[Decimal], Optional[Decimal]]:
        return self._repository.get_rango_precios()

    def anios(self) -> List[int]:
        return self._repository.get_anios()

    def condiciones(self) -> List[str]:
        return self._repository.get_condiciones()

    def rango_kilometraje(self) -> Tuple[Optional[int], Optional[int]]:
        return self._repository.get_rango_kilometraje()
