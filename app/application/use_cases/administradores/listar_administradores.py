from typing import List

from app.application.dto.administrador_dto import AdministradorResponseDTO
from app.domain.repositories.administrador_repository import AdministradorRepository


class ListarAdministradoresUseCase:
    def __init__(self, repository: AdministradorRepository):
        self._repository = repository

    def execute(self) -> List[AdministradorResponseDTO]:
        administradores = self._repository.get_all()
        return [
            AdministradorResponseDTO(
                id=a.id,
                nombre=a.nombre,
                correo=a.correo,
                activo=a.activo,
                creado_en=a.creado_en,
                actualizado_en=a.actualizado_en,
            )
            for a in administradores
        ]
