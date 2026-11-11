from app.application.dto.vehiculo_dto import ActualizarVehiculoDTO, VehiculoResponseDTO
from app.core.exceptions import VehiculoNotFoundError
from app.domain.repositories.vehiculo_repository import VehiculoRepository


class ActualizarVehiculoUseCase:
    def __init__(self, repository: VehiculoRepository):
        self._repository = repository

    def execute(self, vehiculo_id: int, dto: ActualizarVehiculoDTO) -> VehiculoResponseDTO:
        vehiculo = self._repository.get_by_id(vehiculo_id)
        if not vehiculo:
            raise VehiculoNotFoundError(vehiculo_id)

        if dto.condicion is not None:
            vehiculo.condicion = dto.condicion
        if dto.marca is not None:
            vehiculo.marca = dto.marca
        if dto.modelo is not None:
            vehiculo.modelo = dto.modelo
        if dto.anio is not None:
            vehiculo.anio = dto.anio
        if dto.precio is not None:
            vehiculo.precio = dto.precio
        if dto.kilometraje is not None:
            vehiculo.kilometraje = dto.kilometraje
        if dto.transmision is not None:
            vehiculo.transmision = dto.transmision
        if dto.combustible is not None:
            vehiculo.combustible = dto.combustible
        if dto.descripcion is not None:
            vehiculo.descripcion = dto.descripcion
        if dto.fotoauto is not None:
            vehiculo.fotoauto = dto.fotoauto
        if dto.estado is not None:
            vehiculo.estado = dto.estado

        updated = self._repository.update(vehiculo)
        return VehiculoResponseDTO(
            id=updated.id,
            condicion=updated.condicion,
            marca=updated.marca,
            modelo=updated.modelo,
            anio=updated.anio,
            precio=updated.precio,
            kilometraje=updated.kilometraje,
            transmision=updated.transmision,
            combustible=updated.combustible,
            descripcion=updated.descripcion,
            fotoauto=updated.fotoauto,
            estado=updated.estado,
            creado_en=updated.creado_en,
            actualizado_en=updated.actualizado_en,
        )
