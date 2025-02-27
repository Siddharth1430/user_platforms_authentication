from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import User, Credential, Platform
from app.database.connection import get_db
from app.auth.auth import admin_authenticate
from app.database.schemas import (
    UserResponseSchema,
    PlatformResponseSchema,
    CredentialResponseSchema,
)
from typing import List

router = APIRouter()


# Get details of all users:
@router.get("/users", response_model=List[UserResponseSchema])
def get_users(
    admin: User = Depends(admin_authenticate), db: Session = Depends(get_db)
) -> List[User]:
    """
    This route will return the details of all users after verfiying user has admin access
    """
    return db.query(User).all()


# Get details of one user :
@router.get("/users/{user_id}", response_model=UserResponseSchema)
def get_one_user(
    user_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
) -> User:
    """
    This route will return the details of one user after verifying that user has admin access
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# Get all platforms a user is integrated with :
@router.get("/users/{user_id}/platforms")
def get_platforms_for_user(
    user_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    """
    This route will return all platforms that a user in integrated with
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    platforms_list = []
    for platform in user.platforms:
        platforms_list.append({"id": platform.id, "name": platform.name})

    return {"user_id": user.id, "platforms": platforms_list}


# Get details of one platform
@router.get("/platforms/{platform_id}", response_model=PlatformResponseSchema)
def get_one_platform(
    platform_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
) -> Platform:
    """
    This route will return the details of a specific platform
    """
    platform = db.query(Platform).filter(Platform.id == platform_id).first()
    if not platform:
        raise HTTPException(status_code=404, detail="Platform not found")

    return platform


# Get the credentials of a user for a specific platform
@router.get(
    "/users/{user_id}/{platform_id}/credentials",
    response_model=CredentialResponseSchema,
)
def get_credentials(
    user_id: int,
    platform_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
) -> Credential:
    """
    This route will return the credentials of a user of a specific platform
    """
    credential = (
        db.query(Credential)
        .filter(Credential.user_id == user_id, Credential.platform_id == platform_id)
        .first()
    )
    if not credential:
        raise HTTPException(status_code=404, detail="Credentials not found")

    return credential
