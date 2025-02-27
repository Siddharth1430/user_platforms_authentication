from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from app.auth.utils import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    SECRET_KEY,
    REFRESH_KEY,
    ALGORITHM,
)
from app.database.connection import get_db
from app.database.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def verify_token(token: str, key: str):
    """
    This function will take the token and verify that it is valid before using it to authenticate or create new access token
    """
    try:
        payload = jwt.decode(token, key, algorithms=ALGORITHM)
        username = str(payload.get("sub"))
        if username is None:
            raise HTTPException(
                status_code=401, detail="Token is invalid, sub claim is missing"
            )
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def user_authenticate(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> User:
    """
    This function will grant authorization if the user exists
    """
    username = verify_token(token, SECRET_KEY)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


def refresh_access_token(token: str, db: Session):
    """
    This function will create a new access token
    """
    username = verify_token(token, REFRESH_KEY)
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    new_access_token = create_access_token({"sub": username}, access_token_expires)
    return {"access token": new_access_token, "token-type": "Bearer"}


def admin_authenticate(user: User = Depends(user_authenticate)) -> User:
    """
    This function will verify that the authenticated user has admin privileges
    """
    # print(user.id, user.username, user.password, user.is_admin)
    if not user.is_admin:  # type: ignore
        raise HTTPException(status_code=401, detail="Invalid, user is not admin")
    return user
