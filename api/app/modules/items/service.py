"""Item business logic — pure Python, no HTTP awareness."""
from datetime import datetime, timezone

from sqlalchemy import select

from app.extensions import db
from app.modules.items.models import Item


class ItemNotFoundError(Exception):
    def __init__(self, item_id: int):
        self.item_id = item_id
        super().__init__(f"Item {item_id} not found")


def create_item(data) -> Item:
    item = Item(**data.model_dump(exclude_unset=True))
    db.session.add(item)
    db.session.commit()
    return item


def get_all_items() -> list[Item]:
    return list(
        db.session.scalars(
            select(Item)
            .where(Item.deleted_at.is_(None))
            .order_by(Item.created_at.desc())
        ).all()
    )


def get_item(item_id: int) -> Item:
    item = db.session.get(Item, item_id)
    if item is None or item.deleted_at is not None:
        raise ItemNotFoundError(item_id)
    return item


def update_item(item_id: int, data) -> Item:
    item = get_item(item_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.session.commit()
    return item


def delete_item(item_id: int) -> None:
    item = get_item(item_id)
    item.deleted_at = datetime.now(timezone.utc)
    db.session.commit()