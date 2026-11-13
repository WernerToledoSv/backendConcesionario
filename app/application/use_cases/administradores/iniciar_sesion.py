from app.application.dto.administrador_dto import AdministradorResponseDTO
from app.core.exceptions import CredencialesInvalidasError
from app.core.security import verify_missing_admin_password, verify_password
from app.domain.repositories.administrador_repository import AdministradorRepository


class IniciarSesionUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, correo: str, password: str) -> AdministradorResponseDTO:
        administrador = self._repository.get_by_correo(correo.strip().lower())
        if administrador is None:
            verify_missing_admin_password(password)
            raise CredencialesInvalidasError()

        password_is_valid = verify_password(password, administrador.password_hash)
        if not administrador.activo or not password_is_valid:
            raise CredencialesInvalidasError()

        return AdministradorResponseDTO(
            id=administrador.id,
            nombre=administrador.nombre,
            correo=administrador.correo,
            activo=administrador.activo,
            creado_en=administrador.creado_en,
            actualizado_en=administrador.actualizado_en,
        )
