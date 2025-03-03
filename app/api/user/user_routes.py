from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.auth import user_authenticate
from app.database.models import User, UserIntegration, Platform, CredentialDetail
from app.database.schemas import (
    CurrentUserResponseSchema,
    PlatformResponseSchema,
    UserIntegrationWithDetailsSchema,
    UserIntegrationSchema,
    UserIntegrationResponseSchema,
    CredentialDetailSchema,
    CredentialDetailResponseSchema,
)
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
def get_platforms(current_user: User = Depends(user_authenticate)):
    """
    This route will get the platforms that current user is integrated with
    """
    return current_user.platforms


# Get the user_integrations of current user
@router.get(
    "/me/user_integrations", response_model=List[UserIntegrationWithDetailsSchema]
)
def get_user_integrations(current_user: User = Depends(user_authenticate)):
    return current_user.credentials


@router.post("/integrate", response_model=UserIntegrationResponseSchema)
def integrate_user(
    integration_data: UserIntegrationSchema,
    credentials: List[CredentialDetailSchema],
    user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
):
    """
    This route will allow the current user to integrate with a platform,store them in user_integrations table and store the credentials in credential_details table
    """
    existing_user = db.query(User).filter(User.id == integration_data.user_id).first()
    existing_platform = (
        db.query(Platform).filter(Platform.id == integration_data.platform_id).first()
    )
    if not existing_user or existing_platform:
        raise HTTPException(status_code=404, detail="User or Platform not found")

    integration = (
        db.query(UserIntegration)
        .filter(
            UserIntegration.user_id == integration_data.user_id,
            UserIntegration.platform_id == integration_data.platform_id,
        )
        .first()
    )

    if not integration:
        integration = UserIntegration(
            user_id=integration_data.user_id,
            platform_id=integration_data.platform_id,
            is_active=integration_data.is_active,
        )
        db.add(integration)

    for cred in credentials:
        credential = CredentialDetail(
            user_id=integration_data.user_id,
            platform_id=integration_data.platform_id,
            integration_id=integration.id,
            key=cred.key,
            value=cred.value,
        )
        db.add(credential)

    db.commit()

    return integration


@router.post("/credentials/", response_model=CredentialDetailResponseSchema)
def add_credential(
    credential_data: CredentialDetailSchema,
    user: User = Depends(user_authenticate),
    db: Session = Depends(get_db),
):
    integration = (
        db.query(UserIntegration)
        .filter(
            UserIntegration.user_id == credential_data.user_id,
            UserIntegration.platform_id == credential_data.platform_id,
        )
        .first()
    )

    if not integration:
        raise HTTPException(status_code=404, detail="Integration not found")

    credential = CredentialDetail(
        user_id=credential_data.user_id,
        platform_id=credential_data.platform_id,
        integration_id=integration.id,
        key=credential_data.key,
        value=credential_data.value,
    )

    db.add(credential)
    db.commit()

    return credential


# @router.post("/me")
# should integrate platfrom with user
# save user_integrations for that platform
# Input - user_id,platform_id,credential_details
# user_id from token, platform_id from fe(int), credential_details from fe
# payload = [{"key":"access_key","value":"absdlkn"}]
# {"access_key":"dkblksn","secret_key":"sddkgln"}
# user_integration = UserIntegration(user_id = user_id,platform_id = platform_id)
# db.add(user_integration)
# for key,value in payload.credentialdetails.items():
#       cred = CredentialDetail(user_id = user_id,platform_id == platform_id,key=key,value=value)
#       db.add(cred)
# for item in payload:
#        item["key"] =
