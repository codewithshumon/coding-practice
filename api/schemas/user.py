from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ── Base — shared fields ──
class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr


# ── Create — what the client sends ──
class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)


# ── Update — all optional ──
class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    email: EmailStr | None = None
    password: str | None = Field(None, min_length=8, max_length=128)
    is_active: bool | None = None


# ── Read — what the client gets back ──
class UserRead(UserBase):
    id: UUID
    is_active: bool

    model_config = {"from_attributes": True}
