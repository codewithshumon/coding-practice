from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field, model_validator


class CreateItemSchema(BaseModel):
    model_config = {"extra": "forbid"}

    name: str = Field(..., min_length=1, max_length=255, examples=["Laptop"])
    price: Decimal = Field(..., ge=0, examples=[999.99])
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = True


class UpdateItemSchema(BaseModel):
    model_config = {"extra": "forbid"}

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[Decimal] = Field(None, ge=0)
    description: Optional[str] = Field(None, max_length=1000)
    in_stock: Optional[bool] = None

    @model_validator(mode="after")
    def at_least_one_field(self):
        if all(v is None for v in self.__dict__.values()):
            raise ValueError("At least one field must be provided for update")
        return self