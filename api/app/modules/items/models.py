from app.extensions import db
from app.common.models.base import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    name = db.Column(db.String(255), nullable=False, index=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    in_stock = db.Column(db.Boolean, nullable=False, default=True, server_default="true")

    def __repr__(self):
        return f"<Item {self.id}: {self.name}>"