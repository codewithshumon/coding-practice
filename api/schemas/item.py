from pydantic import BaseModel, Field
from uuid import UUID

class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=500)
    in_stock: bool = True

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    price: float | None = Field(None, gt=0)
    description: str | None = Field(None, max_length=500)
    in_stock: bool | None = None

class ItemRead(ItemBase):
    id: UUID   # ← was int
    model_config = {"from_attributes": True}
