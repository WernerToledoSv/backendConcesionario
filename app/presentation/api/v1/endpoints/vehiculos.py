from decimal import Decimal
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from app.application.dto.vehiculo_dto import (
    ActualizarVehiculoDTO,
    CrearVehiculoDTO,
    VehiculoResponseDTO,
)
from app.application.use_cases.vehiculos.actualizar_vehiculo import ActualizarVehiculoUseCase
from app.application.use_cases.vehiculos.crear_vehiculo import CrearVehiculoUseCase
from app.application.use_cases.vehiculos.eliminar_vehiculo import EliminarVehiculoUseCase
from app.application.use_cases.vehiculos.listar_vehiculos import ListarVehiculosUseCase
from app.application.use_cases.vehiculos.obtener_vehiculo import ObtenerVehiculoUseCase
from app.core.config import settings
from app.core.exceptions import VehiculoNotFoundError
from app.infrastructure.cloudinary.cloudinary_service import CloudinaryService
from app.infrastructure.repositories.sqlalchemy_vehiculo_repository import SQLAlchemyVehiculoRepository
from app.presentation.api.v1.dependencies import get_cloudinary_service, get_vehiculo_repository
from app.presentation.api.v1.schemas.response_schema import ResponseBase, ResponseItem, ResponseItems
from app.presentation.api.v1.schemas.vehiculo_schema import VehiculoResponse, VehiculoUpdateRequest

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])

# ------------------------------------------------------------------ type aliases
RepoDep = Annotated[SQLAlchemyVehiculoRepository, Depends(get_vehiculo_repository)]
CloudDep = Annotated[CloudinaryService, Depends(get_cloudinary_service)]

MAX_IMAGE_SIZE_BYTES = settings.MAX_IMAGE_SIZE_MB * 1024 * 1024


# ------------------------------------------------------------------ helper
def _to_response(dto: VehiculoResponseDTO) -> VehiculoResponse:
    return VehiculoResponse(
        id=dto.id,
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
        creado_en=dto.creado_en,
        actualizado_en=dto.actualizado_en,
    )


async def _upload_vehicle_image(
    fotoauto: UploadFile,
    cloudinary_svc: CloudinaryService,
) -> str:
    try:
        contenido = await fotoauto.read(MAX_IMAGE_SIZE_BYTES + 1)
        if len(contenido) > MAX_IMAGE_SIZE_BYTES:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail={
                    "code": 0,
                    "message": (
                        f"La imagen no puede superar los "
                        f"{settings.MAX_IMAGE_SIZE_MB} MB."
                    ),
                },
            )
        return cloudinary_svc.upload_image(contenido)
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail={"code": 0, "message": f"Error al subir la imagen: {str(exc)}"},
        )


# ------------------------------------------------------------------ endpoints
@router.post(
    "/CrearVehiculo",
    response_model=ResponseItem[VehiculoResponse],
    status_code=status.HTTP_201_CREATED,
    summary="Crear un nuevo vehículo",
)
async def crear_vehiculo(
    repo: RepoDep,
    cloudinary_svc: CloudDep,
    condicion: str = Form(default="usado", pattern="^(nuevo|usado)$"),
    marca: str = Form(..., max_length=80),
    modelo: str = Form(..., max_length=100),
    anio: int = Form(..., ge=1900),
    precio: Decimal = Form(..., ge=0),
    kilometraje: int = Form(default=0, ge=0),
    transmision: str = Form(default="automatica", pattern="^(manual|automatica|otra)$"),
    combustible: str = Form(default="gasolina", pattern="^(gasolina|diesel|hibrido|electrico|otro)$"),
    descripcion: Optional[str] = Form(default=None),
    estado: str = Form(default="disponible", pattern="^(disponible|reservado|vendido)$"),
    fotoauto: Optional[UploadFile] = File(default=None),
):
    # Subir imagen a Cloudinary si se proporcionó
    foto_url: Optional[str] = None
    if fotoauto:
        foto_url = await _upload_vehicle_image(fotoauto, cloudinary_svc)

    use_case = CrearVehiculoUseCase(repo)
    dto = CrearVehiculoDTO(
        condicion=condicion,
        marca=marca,
        modelo=modelo,
        anio=anio,
        precio=precio,
        kilometraje=kilometraje,
        transmision=transmision,
        combustible=combustible,
        descripcion=descripcion,
        fotoauto=foto_url,
        estado=estado,
    )
    result = use_case.execute(dto)
    return ResponseItem(
        code=1,
        message="Vehículo creado exitosamente.",
        item=_to_response(result),
    )


@router.get(
    "/ListarVehiculos",
    response_model=ResponseItems[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los vehículos",
)
def listar_vehiculos(repo: RepoDep):
    use_case = ListarVehiculosUseCase(repo)
    items = use_case.execute()
    return ResponseItems(
        code=1,
        message="Registros obtenidos exitosamente.",
        items=[_to_response(v) for v in items],
    )


@router.get(
    "/ObtenerVehiculo/{vehiculo_id}",
    response_model=ResponseItem[VehiculoResponse],
    status_code=status.HTTP_200_OK,
    summary="Obtener un vehículo por ID",
)
def obtener_vehiculo(vehiculo_id: int, repo: RepoDep):
    use_case = ObtenerVehiculoUseCase(repo)
    try:
        result = use_case.execute(vehiculo_id)
    except VehiculoNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseItem(
        code=1,
        message="Vehículo obtenido exitosamente.",
        item=_to_response(result),
    )


@router.put(
    "/ActualizarVehiculo/{vehiculo_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Actualizar un vehículo",
)
async def actualizar_vehiculo(
    vehiculo_id: int,
    repo: RepoDep,
    cloudinary_svc: CloudDep,
    body: VehiculoUpdateRequest,
    fotoauto: Optional[UploadFile] = File(default=None),
):
    foto_url: Optional[str] = None
    if fotoauto:
        foto_url = await _upload_vehicle_image(fotoauto, cloudinary_svc)

    use_case = ActualizarVehiculoUseCase(repo)
    try:
        dto = ActualizarVehiculoDTO(
            condicion=body.condicion,
            marca=body.marca,
            modelo=body.modelo,
            anio=body.anio,
            precio=body.precio,
            kilometraje=body.kilometraje,
            transmision=body.transmision,
            combustible=body.combustible,
            descripcion=body.descripcion,
            fotoauto=foto_url if foto_url else body.fotoauto,
            estado=body.estado,
        )
        use_case.execute(vehiculo_id, dto)
    except VehiculoNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseBase(
        code=1,
        message="Vehículo actualizado exitosamente.",
    )


@router.delete(
    "/EliminarVehiculo/{vehiculo_id}",
    response_model=ResponseBase,
    status_code=status.HTTP_200_OK,
    summary="Eliminar un vehículo",
)
def eliminar_vehiculo(vehiculo_id: int, repo: RepoDep):
    use_case = EliminarVehiculoUseCase(repo)
    try:
        use_case.execute(vehiculo_id)
    except VehiculoNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"code": 0, "message": str(exc)},
        )
    return ResponseBase(
        code=1,
        message="Vehículo eliminado exitosamente.",
    )
