from pydantic import BaseModel, Field

# ── Base fields shared by multiple schemas ──
class ItemBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0)
    description: str | None = Field(None, max_length=500)
    in_stock: bool = True


# ── Used when creating (no id yet) ──
class ItemCreate(ItemBase):
    pass


# ── Used when updating — every field is optional ──
class ItemUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    price: float | None = Field(None, gt=0)
    description: str | None = Field(None, max_length=500)
    in_stock: bool | None = None


# ── Used when reading (includes id, works with ORM) ──
class ItemRead(ItemBase):
    id: int

    model_config = {"from_attributes": True}  # lets Pydantic read SQLAlchemy objects
