from app.core.exceptions import AdministradorNotFoundError
from app.domain.repositories.administrador_repository import AdministradorRepository


class EliminarAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, administrador_id: int) -> None:
        administrador = self._repository.get_by_id(administrador_id)
        if not administrador:
            raise AdministradorNotFoundError(administrador_id)

        self._repository.delete(administrador_id)
