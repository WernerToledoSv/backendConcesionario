from app.core.exceptions import SolicitudNotFoundError
from app.domain.repositories.solicitud_repository import SolicitudRepository


class ActualizarNotasSolicitudUseCase:
    def __init__(self, repository: SolicitudRepository):
        self._repository = repository

    def execute(
        self,
        solicitud_id: int,
        notas_administrador: str | None,
    ) -> None:
        if not self._repository.update_notas_administrador(
            solicitud_id,
            notas_administrador,
        ):
            raise SolicitudNotFoundError(solicitud_id)
