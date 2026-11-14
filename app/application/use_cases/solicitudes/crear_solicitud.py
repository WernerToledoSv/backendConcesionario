from app.application.dto.solicitud_dto import CrearSolicitudDTO
from app.core.exceptions import (
    DuplicateVehiclesInSolicitudError,
    VehiclesNotProvidedError,
)
from app.domain.entities.solicitud_compra import SolicitudCompra
from app.domain.repositories.solicitud_repository import SolicitudRepository


class CrearSolicitudUseCase:
    def __init__(self, repository: SolicitudRepository):
        self._repository = repository

    def execute(self, dto: CrearSolicitudDTO) -> SolicitudCompra:
        if not dto.vehiculos_ids:
            raise VehiclesNotProvidedError()
        if len(dto.vehiculos_ids) != len(set(dto.vehiculos_ids)):
            raise DuplicateVehiclesInSolicitudError()
        return self._repository.create(
            nombre_cliente=dto.nombre_cliente,
            correo_cliente=dto.correo_cliente,
            telefono_cliente=dto.telefono_cliente,
            vehiculos_ids=dto.vehiculos_ids,
            mensaje_cliente=dto.mensaje_cliente,
        )
