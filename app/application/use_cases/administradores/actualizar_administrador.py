from app.application.dto.administrador_dto import ActualizarAdministradorDTO, AdministradorResponseDTO
from app.core.exceptions import AdministradorNotFoundError, AdministradorEmailAlreadyExistsError
from app.domain.repositories.administrador_repository import AdministradorRepository


class ActualizarAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, administrador_id: int, dto: ActualizarAdministradorDTO) -> AdministradorResponseDTO:
        administrador = self._repository.get_by_id(administrador_id)
        if not administrador:
            raise AdministradorNotFoundError(administrador_id)

        if dto.correo and dto.correo != administrador.correo:
            existing = self._repository.get_by_correo(dto.correo)
            if existing:
                raise AdministradorEmailAlreadyExistsError(dto.correo)
            administrador.correo = dto.correo

        if dto.nombre is not None:
            administrador.nombre = dto.nombre

        if dto.password is not None:
            administrador.password_hash = dto.password

        if dto.activo is not None:
            administrador.activo = dto.activo

        updated = self._repository.update(administrador)
        return AdministradorResponseDTO(
            id=updated.id,
            nombre=updated.nombre,
            correo=updated.correo,
            activo=updated.activo,
            creado_en=updated.creado_en,
            actualizado_en=updated.actualizado_en,
        )
