from app.core.exceptions import (
    ConcurrentSolicitudUpdateError,
    InvalidSolicitudStateError,
    InvalidSolicitudTransitionError,
    SolicitudNotFoundError,
)
from app.domain.entities.solicitud_compra import (
    SOLICITUD_ESTADOS,
    TRANSICIONES_SOLICITUD,
)
from app.domain.repositories.solicitud_repository import SolicitudRepository


class ActualizarEstadoSolicitudUseCase:
    def __init__(self, repository: SolicitudRepository):
        self._repository = repository

    def execute(self, solicitud_id: int, estado_nuevo: str) -> None:
        if estado_nuevo not in SOLICITUD_ESTADOS:
            raise InvalidSolicitudStateError(estado_nuevo)

        solicitud = self._repository.get_by_id(solicitud_id)
        if solicitud is None:
            raise SolicitudNotFoundError(solicitud_id)
        if estado_nuevo not in TRANSICIONES_SOLICITUD[solicitud.estado]:
            raise InvalidSolicitudTransitionError(solicitud.estado, estado_nuevo)

        updated = self._repository.update_estado(
            solicitud_id,
            estado_actual=solicitud.estado,
            estado_nuevo=estado_nuevo,
        )
        if not updated:
            if self._repository.get_by_id(solicitud_id) is None:
                raise SolicitudNotFoundError(solicitud_id)
            raise ConcurrentSolicitudUpdateError()
