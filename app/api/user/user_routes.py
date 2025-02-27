from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.auth.auth import user_authenticate
from app.database.models import User, Credential

router = APIRouter()


# Get details of current user
@router.get("/users/me")
def get_current_user(current_user: User = Depends(user_authenticate)):
    platforms_data = []
    for platform in current_user.platforms:
        platforms_data.append({"id": platform.id, "name": platform.name})

    return {
        "Username": current_user.username,
        "Password": current_user.password,
        "Platforms": platforms_data,
    }


# Get details of platforms of current user
@router.get("/users/me/platforms")
def get_platforms(current_user: User = Depends(user_authenticate)):
    platforms_data = []
    for platform in current_user.platforms:
        platforms_data.append(
            {
                "id": platform.id,
                "name": platform.name,
                "description": platform.description,
            }
        )
    return platforms_data


# Get the credentials of current user
@router.get("/users/me/credentials")
def get_credentials(current_user: User = Depends(user_authenticate)):
    credential_data = []
    for credential in current_user.credentials:
        credential_details = []
        for detail in credential.credential_details:
            credential_details.append({"key": detail.key, "value": detail.value})

        credential_data.append(
            {
                "id": credential.id,
                "platform": credential.platform.name,
                "details": credential_details,
            }
        )
    return credential_data
