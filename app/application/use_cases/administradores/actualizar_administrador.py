from app.application.dto.administrador_dto import (
    ActualizarAdministradorDTO,
    AdministradorResponseDTO,
)
from app.core.exceptions import (
    AdministradorEmailAlreadyExistsError,
    AdministradorNotFoundError,
)
from app.core.security import hash_password
from app.domain.repositories.administrador_repository import AdministradorRepository


class ActualizarAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(
        self,
        administrador_id: int,
        dto: ActualizarAdministradorDTO,
    ) -> AdministradorResponseDTO:
        administrador = self._repository.get_by_id(administrador_id)
        if administrador is None:
            raise AdministradorNotFoundError(administrador_id)

        if dto.correo is not None and dto.correo.strip().lower() != administrador.correo:
            correo = dto.correo.strip().lower()
            existing = self._repository.get_by_correo(correo)
            if existing is not None and existing.id != administrador_id:
                raise AdministradorEmailAlreadyExistsError(correo)
            administrador.correo = correo

        if dto.nombre is not None:
            administrador.nombre = dto.nombre
        if dto.password is not None:
            administrador.password_hash = hash_password(dto.password)
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
