from app.application.dto.administrador_dto import AdministradorResponseDTO
from app.core.exceptions import CredencialesInvalidasError
from app.domain.repositories.administrador_repository import AdministradorRepository


class IniciarSesionUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, correo: str, password: str) -> AdministradorResponseDTO:
        administrador = self._repository.get_by_correo(correo)
        if (
            administrador is None
            or not administrador.activo
            or administrador.password != password
        ):
            raise CredencialesInvalidasError()

        return AdministradorResponseDTO(
            id=administrador.id,
            nombre=administrador.nombre,
            correo=administrador.correo,
            activo=administrador.activo,
            creado_en=administrador.creado_en,
            actualizado_en=administrador.actualizado_en,
        )