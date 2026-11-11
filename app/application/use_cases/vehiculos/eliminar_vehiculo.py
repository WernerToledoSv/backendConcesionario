from app.core.exceptions import VehiculoNotFoundError
from app.domain.repositories.vehiculo_repository import VehiculoRepository


class EliminarVehiculoUseCase:
    def __init__(self, repository: VehiculoRepository):
        self._repository = repository

    def execute(self, vehiculo_id: int) -> None:
        vehiculo = self._repository.get_by_id(vehiculo_id)
        if not vehiculo:
            raise VehiculoNotFoundError(vehiculo_id)
        self._repository.delete(vehiculo_id)
