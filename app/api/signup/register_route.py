from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.schemas import UserSchema
from app.database.models import User
from app.auth.password import hash_password
from app.database.schemas import UserResponseSchema

router = APIRouter()


@router.post("/register", response_model=UserResponseSchema)
def register_user(user: UserSchema, db: Session = Depends(get_db)):
    """
    This route will allow users to register
    """
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="username already taken")

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username, password=hashed_password, is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
