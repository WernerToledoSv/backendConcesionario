from app.application.dto.administrador_dto import CrearAdministradorDTO, AdministradorResponseDTO
from app.core.exceptions import AdministradorEmailAlreadyExistsError
from app.domain.entities.administrador import Administrador
from app.domain.repositories.administrador_repository import AdministradorRepository


class CrearAdministradorUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self, dto: CrearAdministradorDTO) -> AdministradorResponseDTO:
        existing = self._repository.get_by_correo(dto.correo)
        if existing:
            raise AdministradorEmailAlreadyExistsError(dto.correo)

        administrador = Administrador(
            id=None,
            nombre=dto.nombre,
            correo=dto.correo,
            password=dto.password,
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
