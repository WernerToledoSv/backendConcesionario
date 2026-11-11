from app.application.dto.vehiculo_dto import VehiculoResponseDTO
from app.core.exceptions import VehiculoNotFoundError
from app.domain.repositories.vehiculo_repository import VehiculoRepository


class ObtenerVehiculoUseCase:
    def __init__(self, repository: VehiculoRepository):
        self._repository = repository

    def execute(self, vehiculo_id: int) -> VehiculoResponseDTO:
        vehiculo = self._repository.get_by_id(vehiculo_id)
        if not vehiculo:
            raise VehiculoNotFoundError(vehiculo_id)

        return VehiculoResponseDTO(
            id=vehiculo.id,
            condicion=vehiculo.condicion,
            marca=vehiculo.marca,
            modelo=vehiculo.modelo,
            anio=vehiculo.anio,
            precio=vehiculo.precio,
            kilometraje=vehiculo.kilometraje,
            transmision=vehiculo.transmision,
            combustible=vehiculo.combustible,
            descripcion=vehiculo.descripcion,
            fotoauto=vehiculo.fotoauto,
            estado=vehiculo.estado,
            creado_en=vehiculo.creado_en,
            actualizado_en=vehiculo.actualizado_en,
        )
