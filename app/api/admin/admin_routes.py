from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from app.database.models import User, CredentialDetail, Platform, CredentialDetail
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
from app.filters.filter import UserFilter, PlatformFilter, CredentialDetailFilter
from typing import List

router = APIRouter(prefix="/admin")


# Get details of all users:
@router.get("/users", response_model=List[UserResponseSchema])
def get_users(
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
    filters: UserFilter = FilterDepends(UserFilter),
) -> List[User]:
    """
    This route will return the details of all users after verfiying user has admin access
    """
    query = db.query(User)
    query = filters.filter(query)
    query = filters.sort(query)
    result = db.execute(query)

    return list(result.scalars())


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
    filters: PlatformFilter = FilterDepends(PlatformFilter),
):
    """
    This route will return all platforms that a user in integrated with
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    query = db.query(Platform).filter(Platform.users.contains(user))
    query = filters.filter(query)
    query = filters.sort(query)
    result = db.execute(query)

    return result


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
    response_model=CredentialDetailResponseSchema,
)
def get_credentials(
    user_id: int,
    platform_id: int,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
    filters: CredentialDetailFilter = FilterDepends(CredentialDetailFilter),
):
    """
    This route will return the credentials of a user of a specific platform
    """
    query = (
        db.query(CredentialDetail)
        .filter(
            CredentialDetail.user_id == user_id,
            CredentialDetail.platform_id == platform_id,
        )
        .first()
    )
    query = filters.filter(query)
    query = filters.sort(query)
    credential = db.execute(query)
    if not credential:
        raise HTTPException(status_code=404, detail="Credentials not found")

    return credential


# Create a platform
@router.post("/platform/", response_model=PlatformResponseSchema)
def add_platform(
    platform_data: PlatformSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    platform = Platform(name=platform_data.name, description=platform_data.description)
    db.add(platform)
    db.commit()

    return platform


@router.post("/user-integration", response_model=UserIntegrationResponseSchema)
def assign_user_to_platform(
    integration_data: UserIntegrationSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    integration = CredentialDetail(
        user_id=integration_data.user_id, platform_id=integration_data.platform_id
    )
    db.add(integration)
    db.commit()

    return integration


@router.post("/credential/", response_model=CredentialDetailResponseSchema)
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
