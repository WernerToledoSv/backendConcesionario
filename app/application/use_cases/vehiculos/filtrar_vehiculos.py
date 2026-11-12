from decimal import Decimal
from typing import List, Optional

from app.application.dto.vehiculo_dto import VehiculoResponseDTO
from app.domain.repositories.catalogo_filtro_vehiculo_repository import (
    CatalogoFiltroVehiculoRepository,
)


class FiltrarVehiculosUseCase:
    def __init__(self, repository: CatalogoFiltroVehiculoRepository):
        self._repository = repository

    def execute(
        self,
        marca: Optional[str] = None,
        transmision: Optional[str] = None,
        combustible: Optional[str] = None,
        precio_minimo: Optional[Decimal] = None,
        precio_maximo: Optional[Decimal] = None,
        anio: Optional[int] = None,
        condicion: Optional[str] = None,
        kilometraje_minimo: Optional[int] = None,
        kilometraje_maximo: Optional[int] = None,
    ) -> List[VehiculoResponseDTO]:
        vehiculos = self._repository.get_filtered(
            marca=marca,
            transmision=transmision,
            combustible=combustible,
            precio_minimo=precio_minimo,
            precio_maximo=precio_maximo,
            anio=anio,
            condicion=condicion,
            kilometraje_minimo=kilometraje_minimo,
            kilometraje_maximo=kilometraje_maximo,
        )
        return [
            VehiculoResponseDTO(
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
            for vehiculo in vehiculos
        ]
