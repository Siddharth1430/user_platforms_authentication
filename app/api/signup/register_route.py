from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.schemas import UserSchema
from app.database.models import User

router = APIRouter()


@router.post("/register")
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    """
    This route will allow users to register
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username already taken")
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
