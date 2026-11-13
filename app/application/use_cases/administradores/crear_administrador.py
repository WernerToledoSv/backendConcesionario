from app.application.dto.administrador_dto import (
    AdministradorResponseDTO,
    CrearAdministradorDTO,
)
from app.core.exceptions import AdministradorEmailAlreadyExistsError
from app.core.security import hash_password
from app.domain.entities.administrador import Administrador
from app.domain.repositories.administrador_repository import AdministradorRepository


class CrearAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, dto: CrearAdministradorDTO) -> AdministradorResponseDTO:
        correo = dto.correo.strip().lower()
        if self._repository.get_by_correo(correo):
            raise AdministradorEmailAlreadyExistsError(correo)

        administrador = Administrador(
            id=None,
            nombre=dto.nombre,
            correo=correo,
            password_hash=hash_password(dto.password),
        )
        saved = self._repository.save(administrador)
        return AdministradorResponseDTO(
            id=saved.id,
            nombre=saved.nombre,
            correo=saved.correo,
            activo=saved.activo,
            creado_en=saved.creado_en,
            actualizado_en=saved.actualizado_en,
        )
