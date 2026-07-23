from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from models.item import Item
from schemas.item import ItemCreate, ItemUpdate, ItemRead

router = APIRouter(prefix="/items", tags=["Items"])


# ── GET /items — list all ──────────────────────────────────
@router.get("/", response_model=list[ItemRead])
def list_items(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    items = db.query(Item).offset(skip).limit(limit).all()
    return items


# ── GET /items/{item_id} — get one ─────────────────────────
@router.get("/{item_id}", response_model=ItemRead)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ── POST /items — create ───────────────────────────────────
@router.post("/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
def create_item(item_in: ItemCreate, db: Session = Depends(get_db)):
    new_item = Item(**item_in.model_dump())  # Pydantic dict → SQLAlchemy model
    db.add(new_item)
    db.commit()
    db.refresh(new_item)  # gets the auto-generated id
    return new_item


# ── PUT /items/{item_id} — full replace ────────────────────
@router.put("/{item_id}", response_model=ItemRead)
def replace_item(item_id: int, item_in: ItemCreate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Replace every field
    for field, value in item_in.model_dump().items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


# ── PATCH /items/{item_id} — partial update ─────────────────
@router.patch("/{item_id}", response_model=ItemRead)
def patch_item(item_id: int, item_in: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Only update fields the client actually sent
    for field, value in item_in.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)
    return item


# ── DELETE /items/{item_id} — remove ────────────────────────
@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    # 204 = no body, so no return
