from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.application.dto.administrador_dto import (
    ActualizarAdministradorDTO,
    AdministradorResponseDTO,
    CrearAdministradorDTO,
)
from app.application.use_cases.administradores.actualizar_administrador import (
    ActualizarAdministradorUseCase,
)
from app.application.use_cases.administradores.crear_administrador import (
    CrearAdministradorUseCase,
)
from app.application.use_cases.administradores.eliminar_administrador import (
    EliminarAdministradorUseCase,
)
from app.application.use_cases.administradores.iniciar_sesion import (
    IniciarSesionUseCase,
)
from app.application.use_cases.administradores.listar_administradores import (
    ListarAdministradoresUseCase,
)
from app.application.use_cases.administradores.obtener_administrador import (
    ObtenerAdministradorUseCase,
)
from app.core.exceptions import (
    AdministradorEmailAlreadyExistsError,
    AdministradorNotFoundError,
    CredencialesInvalidasError,
)
from app.infrastructure.repositories.sqlalchemy_administrador_repository import (
    SQLAlchemyAdministradorRepository,
)
from app.infrastructure.security.jwt_service import create_access_token
from app.presentation.api.v1.dependencies import (
    get_administrador_repository,
    get_current_admin,
)
from app.presentation.api.v1.schemas.administrador_schema import (
    AdministradorCreateRequest,
    AdministradorLoginRequest,
    AdministradorResponse,
    AdministradorUpdateRequest,
    LoginResponse,
)
from app.presentation.api.v1.schemas.response_schema import (
    ResponseBase,
    ResponseItem,
    ResponseItems,
)

router = APIRouter(prefix="/administradores", tags=["Administradores"])
RepoDep = Annotated[
    SQLAlchemyAdministradorRepository,
    Depends(get_administrador_repository),
]


def _to_response(dto: AdministradorResponseDTO) -> AdministradorResponse:
    return AdministradorResponse(
        id=dto.id,
        nombre=dto.nombre,
        correo=dto.correo,
        activo=dto.activo,
        creado_en=dto.creado_en,
        actualizado_en=dto.actualizado_en,
    )


@router.post(
    "/IniciarSesion",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión como administrador",
)
def iniciar_sesion(body: AdministradorLoginRequest, repo: RepoDep):
    try:
        result = IniciarSesionUseCase(repo).execute(body.correo, body.password)
    except CredencialesInvalidasError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 0, "message": "Correo o contraseña incorrectos."},
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    token, expires_in = create_access_token(str(result.id))
    return LoginResponse(
        code=1,
        message="Inicio de sesión exitoso.",
        item=_to_response(result),
        access_token=token,
        token_type="bearer",
        expires_in=expires_in,
    )


@router.post(
    "/CrearAdministrador",
    response_model=ResponseItem[AdministradorResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo administrador",
    dependencies=[Depends(get_current_admin)],
)
def crear_administrador(
    body: AdministradorCreateRequest,
    repo: RepoDep,
):
    try:
        dto = CrearAdministradorDTO(
            nombre=body.nombre,
            correo=body.correo,
            password=body.password,
        )
        result = CrearAdministradorUseCase(repo).execute(dto)
    except AdministradorEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 0, "message": str(exc)},
        ) from exc
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
    dependencies=[Depends(get_current_admin)],
)
def listar_administradores(repo: RepoDep):
    items = ListarAdministradoresUseCase(repo).execute()
    return ResponseItems(
        code=1,
        message="Registros obtenidos exitosamente.",
        items=[_to_response(admin) for admin in items],
    )


@router.get(
    "/ObtenerAdministrador/{administrador_id}",
    response_model=ResponseItem[AdministradorResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener un administrador por ID",
    dependencies=[Depends(get_current_admin)],
)
def obtener_administrador(
    administrador_id: int,
    repo: RepoDep,
):
    try:
        result = ObtenerAdministradorUseCase(repo).execute(administrador_id)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc
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
    dependencies=[Depends(get_current_admin)],
)
def actualizar_administrador(
    administrador_id: int,
    body: AdministradorUpdateRequest,
    repo: RepoDep,
):
    try:
        dto = ActualizarAdministradorDTO(
            nombre=body.nombre,
            correo=body.correo,
            password=body.password,
            activo=body.activo,
        )
        ActualizarAdministradorUseCase(repo).execute(administrador_id, dto)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    except AdministradorEmailAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    return ResponseBase(
        code=1,
        message="Administrador actualizado exitosamente.",
    )


@router.delete(
    "/EliminarAdministrador/{administrador_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Eliminar un administrador",
    dependencies=[Depends(get_current_admin)],
)
def eliminar_administrador(
    administrador_id: int,
    repo: RepoDep,
):
    try:
        EliminarAdministradorUseCase(repo).execute(administrador_id)
    except AdministradorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        ) from exc
    return ResponseBase(
        code=1,
        message="Administrador eliminado exitosamente.",
    )
