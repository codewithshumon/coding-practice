from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status 
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import User
from schemas.user import UserCreate, UserUpdate, UserRead

router = APIRouter(prefix="/users", tags=["Users"])


@router.get('/', response_model=list[UserRead])
def list_users(skip: int = 0, limit = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users