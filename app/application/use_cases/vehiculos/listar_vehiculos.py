from typing import List

from app.application.dto.vehiculo_dto import VehiculoResponseDTO
from app.domain.repositories.vehiculo_repository import VehiculoRepository


class ListarVehiculosUseCase:
    def __init__(self, repository: VehiculoRepository):
        self._repository = repository

    def execute(self) -> List[VehiculoResponseDTO]:
        vehiculos = self._repository.get_all()
        return [
            VehiculoResponseDTO(
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
            for v in vehiculos
        ]
