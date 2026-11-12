from typing import List

from app.application.dto.solicitud_dto import (
    DetalleSolicitudResponseDTO,
    SolicitudCompraResponseDTO,
)
from app.domain.repositories.solicitud_repository import SolicitudRepository


class ListarSolicitudesUseCase:
    def __init__(self, repository: SolicitudRepository):
        self._repository = repository

    def execute(self) -> List[SolicitudCompraResponseDTO]:
        return [
            SolicitudCompraResponseDTO(
                id=solicitud.id,
                nombre_cliente=solicitud.nombre_cliente,
                correo_cliente=solicitud.correo_cliente,
                telefono_cliente=solicitud.telefono_cliente,
                estado=solicitud.estado,
                total_estimado=solicitud.total_estimado,
                mensaje_cliente=solicitud.mensaje_cliente,
                notas_administrador=solicitud.notas_administrador,
                creado_en=solicitud.creado_en,
                actualizado_en=solicitud.actualizado_en,
                detalles=[
                    DetalleSolicitudResponseDTO(
                        id=detalle.id,
                        vehiculo_id=detalle.vehiculo_id,
                        precio_unitario=detalle.precio_unitario,
                        marca=detalle.marca,
                        modelo=detalle.modelo,
                        anio=detalle.anio,
                        fotoauto=detalle.fotoauto,
                    )
                    for detalle in solicitud.detalles
                ],
            )
            for solicitud in self._repository.get_all()
        ]