from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ResponseBase(BaseModel):
    """Respuesta sin datos: solo código y mensaje. Usar para crear, actualizar y eliminar."""
    code: int
    message: str


class ResponseItem(ResponseBase, Generic[T]):
    """Respuesta con un único objeto."""
    item: T


class ResponseItems(ResponseBase, Generic[T]):
    """Respuesta con una colección de objetos."""
    items: List[T]
