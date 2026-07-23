from sqlalchemy import Column, Integer, String, Float, Boolean
from db.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    price = Column(Float, nullable=False)
    description = Column(String(500), nullable=True)
    in_stock = Column(Boolean, default=True)
