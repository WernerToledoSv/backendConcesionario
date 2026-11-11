from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.administrador_dto import (
    ActualizarAdministradorDTO,
    AdministradorResponseDTO,
    CrearAdministradorDTO,
)
from app.application.use_cases.administradores.actualizar_administrador import ActualizarAdministradorUseCase
from app.application.use_cases.administradores.crear_administrador import CrearAdministradorUseCase
from app.application.use_cases.administradores.eliminar_administrador import EliminarAdministradorUseCase
from app.application.use_cases.administradores.listar_administradores import ListarAdministradoresUseCase
from app.application.use_cases.administradores.obtener_administrador import ObtenerAdministradorUseCase
from app.core.exceptions import AdministradorEmailAlreadyExistsError, AdministradorNotFoundError
from app.infrastructure.repositories.sqlalchemy_administrador_repository import SQLAlchemyAdministradorRepository
from app.presentation.api.v1.dependencies import get_administrador_repository
from app.presentation.api.v1.schemas.administrador_schema import (
    AdministradorCreateRequest,
    AdministradorResponse,
    AdministradorUpdateRequest,
)
from app.presentation.api.v1.schemas.response_schema import ResponseBase, ResponseItem, ResponseItems

router = APIRouter(prefix="/administradores", tags=["Administradores"])

# ------------------------------------------------------------------ type aliases
RepoDep = Annotated[SQLAlchemyAdministradorRepository, Depends(get_administrador_repository)]


# ------------------------------------------------------------------ helper
def _to_response(dto: AdministradorResponseDTO) -> AdministradorResponse:
    return AdministradorResponse(
        id=dto.id,
        nombre=dto.nombre,
        correo=dto.correo,
        activo=dto.activo,
        creado_en=dto.creado_en,
        actualizado_en=dto.actualizado_en,
    )


# ------------------------------------------------------------------ endpoints
@router.post(
    "/CrearAdministrador",
    response_model=ResponseItem[AdministradorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo administrador",
)
def crear_administrador(body: AdministradorCreateRequest, repo: RepoDep):
    use_case = CrearAdministradorUseCase(repo)
    try:
        dto = CrearAdministradorDTO(nombre=body.nombre, correo=body.correo, password=body.password)
        result = use_case.execute(dto)
    except AdministradorEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseItem(
        code=1,
        message="Administrador creado exitosamente.",
        item=_to_response(result),
    )


@router.get(
    "/ListarAdministradores",
    response_model=ResponseItems[AdministradorResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los administradores",
)
def listar_administradores(repo: RepoDep):
    use_case = ListarAdministradoresUseCase(repo)
    items = use_case.execute()
    return ResponseItems(
        code=1,
        message="Registros obtenidos exitosamente.",
        items=[_to_response(a) for a in items],
    )


@router.get(
    "/ObtenerAdministrador/{administrador_id}",
    response_model=ResponseItem[AdministradorResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener un administrador por ID",
)
def obtener_administrador(administrador_id: int, repo: RepoDep):
    use_case = ObtenerAdministradorUseCase(repo)
    try:
        result = use_case.execute(administrador_id)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseItem(
        code=1,
        message="Administrador obtenido exitosamente.",
        item=_to_response(result),
    )


@router.put(
    "/ActualizarAdministrador/{administrador_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un administrador",
)
def actualizar_administrador(
    administrador_id: int,
    body: AdministradorUpdateRequest,
    repo: RepoDep,
):
    use_case = ActualizarAdministradorUseCase(repo)
    try:
        dto = ActualizarAdministradorDTO(
            nombre=body.nombre,
            correo=body.correo,
            password=body.password,
            activo=body.activo,
        )
        use_case.execute(administrador_id, dto)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    except AdministradorEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseBase(
        code=1,
        message="Administrador actualizado exitosamente.",
    )


@router.delete(
    "/EliminarAdministrador/{administrador_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Eliminar un administrador",
)
def eliminar_administrador(administrador_id: int, repo: RepoDep):
    use_case = EliminarAdministradorUseCase(repo)
    try:
        use_case.execute(administrador_id)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseBase(
        code=1,
        message="Administrador eliminado exitosamente.",
    )
