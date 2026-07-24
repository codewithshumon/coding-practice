import uuid
from sqlalchemy import Column, String, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from db.database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    in_stock = Column(Boolean, default=True)
