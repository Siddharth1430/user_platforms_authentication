from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from app.auth.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    REFRESH_TOKEN_EXPIRE_DAYS,
    create_refresh_token,
)
from app.database.connection import get_db
from app.database.schemas import UserSchema
from app.database.models import User
from app.auth.password import verify_password

router = APIRouter()


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    This route will allow users to login with their username and password to recieve their
    access token
    """
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username")

    hashed_password = str(user.password)
    if not verify_password(data.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires=access_token_expires
    )
    refresh_token_expires = timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = create_refresh_token(
        data={"sub": user.username}, expires=refresh_token_expires
    )

    return {
        "Access Token": access_token,
        "Refresh Token": refresh_token,
        "Token type": "Bearer",
    }
