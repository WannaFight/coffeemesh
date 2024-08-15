import datetime
import uuid
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, Field, field_validator, validator


class Size(Enum):
    small = "small"
    medium = "medium"
    big = "big"


class Status(Enum):
    created = "created"
    progress = "progress"
    cancelled = "cancelled"
    dispatched = "dispatched"
    delivered = "delivered"


class OrderItemSchema(BaseModel):
    product: str
    size: Size
    quantity: Annotated[int, Field(strict=True, ge=1)] | None = 1

    @field_validator("quantity")
    @classmethod
    def quantity_not_nullable(cls, value):
        if value is None:
            raise ValueError("quantity may not be None")
        return value


class CreateOrderSchema(BaseModel):
    order: Annotated[list[OrderItemSchema], Field(min_length=1)]


class GetOrderSchema(CreateOrderSchema):
    id: uuid.UUID
    created: datetime.datetime
    status: Status


class GetOrdersSchema(BaseModel):
    orders: list[GetOrderSchema]
