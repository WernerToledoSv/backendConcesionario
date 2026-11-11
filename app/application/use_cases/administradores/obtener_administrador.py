from app.application.dto.administrador_dto import AdministradorResponseDTO
from app.core.exceptions import AdministradorNotFoundError
from app.domain.repositories.administrador_repository import AdministradorRepository


class ObtenerAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, administrador_id: int) -> AdministradorResponseDTO:
        administrador = self._repository.get_by_id(administrador_id)
        if not administrador:
            raise AdministradorNotFoundError(administrador_id)

        return AdministradorResponseDTO(
            id=administrador.id,
            nombre=administrador.nombre,
            correo=administrador.correo,
            activo=administrador.activo,
            creado_en=administrador.creado_en,
            actualizado_en=administrador.actualizado_en,
        )
