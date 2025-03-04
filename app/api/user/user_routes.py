from fastapi import APIRouter, Depends, HTTPException
from fastapi_filter import FilterDepends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.auth import user_authenticate
from app.database.models import User, CredentialDetail, Platform, CredentialDetail
from app.database.schemas import (
    CurrentUserResponseSchema,
    PlatformResponseSchema,
    UserIntegrationWithDetailsSchema,
    UserIntegrationSchema,
    UserIntegrationResponseSchema,
    CredentialDetailSchema,
    CredentialDetailResponseSchema,
    CredentialIntegration,
)
from app.filters.filter import PlatformFilter, UserIntegrationFilter
from app.service.users.post.integration import IntegrationServices
from app.service.users.post.credential import CredentialServices
from app.service.users.get.platform_get import PlatformGetServices
from app.service.users.get.integration_get import IntegrationGetServices
from typing import List

router = APIRouter(prefix="/users")


# Get details of current user
@router.get("/me", response_model=CurrentUserResponseSchema)
def get_current_user(current_user: User = Depends(user_authenticate)):
    """
    This route will get the details of current user
    """
    return current_user


# Get details of platforms of current user
@router.get("/me/platforms", response_model=List[PlatformResponseSchema])
def get_platforms(
    current_user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
    filters: PlatformFilter = FilterDepends(PlatformFilter),
):
    """
    This route will get the platforms that current user is integrated with
    """
    platform_service = PlatformGetServices(db)
    return platform_service.get_user_platforms(current_user, filters)


# Get the user_integrations of current user
@router.get(
    "/me/user_integrations", response_model=List[UserIntegrationWithDetailsSchema]
)
def get_user_integrations(
    current_user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
    filters: UserIntegrationFilter = FilterDepends(UserIntegrationFilter),
):
    integration_service = IntegrationGetServices(db)
    return integration_service.get_user_integrations(current_user, filters)


@router.post("/integrate", response_model=UserIntegrationResponseSchema)
def integrate_user(
    integrate_cred: CredentialIntegration,
    user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
):
    """
    This route will allow the current user to integrate with a platform,store them in user_integrations table and store the credentials in credential_details table
    """
    integration_service = IntegrationServices(db, integrate_cred, user)
    response = integration_service.integrate()
    return response


@router.post("/credentials/", response_model=CredentialDetailResponseSchema)
def add_credential(
    credential_data: CredentialDetailSchema,
    user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
):
    """
    This route will allow the current user to add credentials to the CredentialDetail model
    """
    credential_service = CredentialServices(db, user, credential_data)
    response = credential_service.cred_service()
    return response
