from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class RangoPreciosResponse(BaseModel):
    minimo: Optional[Decimal]
    maximo: Optional[Decimal]


class RangoKilometrajeResponse(BaseModel):
    minimo: Optional[int]
    maximo: Optional[int]
