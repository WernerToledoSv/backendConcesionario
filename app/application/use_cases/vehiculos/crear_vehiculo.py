from app.application.dto.vehiculo_dto import CrearVehiculoDTO, VehiculoResponseDTO
from app.domain.entities.vehiculo import Vehiculo
from app.domain.repositories.vehiculo_repository import VehiculoRepository


class CrearVehiculoUseCase:
    def __init__(self, repository: VehiculoRepository):
        self._repository = repository

    def execute(self, dto: CrearVehiculoDTO) -> VehiculoResponseDTO:
        vehiculo = Vehiculo(
            id=None,
            condicion=dto.condicion,
            marca=dto.marca,
            modelo=dto.modelo,
            anio=dto.anio,
            precio=dto.precio,
            kilometraje=dto.kilometraje,
            transmision=dto.transmision,
            combustible=dto.combustible,
            descripcion=dto.descripcion,
            fotoauto=dto.fotoauto,
            estado=dto.estado,
        )
        saved = self._repository.save(vehiculo)
        return self._to_dto(saved)

    @staticmethod
    def _to_dto(v: Vehiculo) -> VehiculoResponseDTO:
        return VehiculoResponseDTO(
            id=v.id,
            condicion=v.condicion,
            marca=v.marca,
            modelo=v.modelo,
            anio=v.anio,
            precio=v.precio,
            kilometraje=v.kilometraje,
            transmision=v.transmision,
            combustible=v.combustible,
            descripcion=v.descripcion,
            fotoauto=v.fotoauto,
            estado=v.estado,
            creado_en=v.creado_en,
            actualizado_en=v.actualizado_en,
        )
