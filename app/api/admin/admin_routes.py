from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from app.database.models import User, Platform, CredentialDetail, UserIntegration
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
    AdminIntegrationSchema,
    AdminCredentialDetailSchema,
)
from app.filters.filter import UserFilter, PlatformFilter, CredentialDetailFilter
from app.service.admins.get.user_service import UserService
from app.service.admins.get.platform_service import PlatformService
from app.service.admins.get.credential_service import CredentialService
from app.service.admins.post.integration_post import IntegrationPostService
from app.service.admins.post.credential_post import CredentialPostService
from app.service.admins.post.platform_post import PlatformPostService
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
    user_service = UserService(db)
    return user_service.get_all_users(filters)


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
    user_service = UserService(db)
    user = user_service.get_user_by_id(user_id)
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
    platform_service = PlatformService(db)
    platforms = platform_service.get_user_platforms(user_id, filters)
    if platforms is None:
        raise HTTPException(status_code=404, detail="User not found")
    return platforms


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
    platform_service = PlatformService(db)
    platform = platform_service.get_platform_by_id(platform_id)
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
    credential_service = CredentialService(db)
    credentials = credential_service.get_user_credentials(user_id, platform_id, filters)
    if not credentials:
        raise HTTPException(status_code=404, detail="Credentials not found")
    return credentials


# Create a platform
@router.post("/platform/", response_model=PlatformResponseSchema)
def add_platform(
    platform_data: PlatformSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    """
    This route will allow an admin to create a platform
    """
    platform_service = PlatformPostService(db)
    return platform_service.create_platform(platform_data)


@router.post("/user-integration", response_model=UserIntegrationResponseSchema)
def assign_user_to_platform(
    integration_data: AdminIntegrationSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    """
    Assigns a user to a platform, integrating them into it.
    """
    integration_service = IntegrationPostService(db)
    return integration_service.assign_user(integration_data)


@router.post("/credential/", response_model=CredentialDetailResponseSchema)
def add_credential(
    credential_data: AdminCredentialDetailSchema,
    admin: User = Depends(admin_authenticate),
    db: Session = Depends(get_db),
):
    """
    Adds credentials for a user's integration with a platform.
    """
    credential_service = CredentialPostService(db)
    return credential_service.add_credential(credential_data)
