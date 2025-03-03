from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.models import User, UserIntegration, Platform, CredentialDetail
from app.database.connection import get_db
from app.auth.auth import admin_authenticate
from app.database.schemas import (
    UserResponseSchema,
    PlatformSchema,
    PlatformResponseSchema,
    UserIntegrationSchema,
    UserIntegrationResponseSchema,
    CurrentUserResponseSchema,
    CredentialDetailSchema,
    CredentialDetailResponseSchema,
)
from typing import List

router = APIRouter(prefix="/admin")


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
@router.get("/users/{user_id}/platforms", response_model=CurrentUserResponseSchema)
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

    return user


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
    response_model=UserIntegrationResponseSchema,
)
def get_credentials(
    user_id: int,
    platform_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
) -> UserIntegration:
    """
    This route will return the credentials of a user of a specific platform
    """
    credential = (
        db.query(UserIntegration)
        .filter(
            UserIntegration.user_id == user_id,
            UserIntegration.platform_id == platform_id,
        )
        .first()
    )
    if not credential:
        raise HTTPException(status_code=404, detail="Credentials not found")

    return credential


# Create a platform
@router.post("/platforms/", response_model=PlatformResponseSchema)
def add_platform(
    platform_data: PlatformSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    platform = Platform(name=platform_data.name, description=platform_data.description)
    db.add(platform)
    db.commit()

    return platform


@router.post("/user-integrations", response_model=UserIntegrationResponseSchema)
def assign_user_to_platform(
    integration_data: UserIntegrationSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    integration = UserIntegration(
        user_id=integration_data.user_id, platform_id=integration_data.platform_id
    )
    db.add(integration)
    db.commit()

    return integration


@router.post("/credentials/", response_model=CredentialDetailResponseSchema)
def add_credential(
    credential_data: CredentialDetailSchema,
    admin: User = Depends(get_db),
    db: Session = Depends(get_db),
):
    credential = CredentialDetail(
        user_id=credential_data.user_id,
        platform_id=credential_data.platform_id,
        key=credential_data.key,
        value=credential_data.value,
    )
    db.add(credential)
    db.commit()

    return credential


# @router.post("/platform",status_code=201)
# def add_platform()
