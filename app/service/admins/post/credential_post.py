from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.models import CredentialDetail, UserIntegration
from app.database.schemas import CredentialDetailSchema, AdminCredentialDetailSchema


class CredentialPostService:
    def __init__(self, db: Session):
        self.db = db

    def add_credential(self, credential_data: AdminCredentialDetailSchema):
        """
        Adds a credential for a user's platform integration
        """
        integration = (
            self.db.query(UserIntegration)
            .filter(
                UserIntegration.user_id == credential_data.user_id,
                UserIntegration.platform_id == credential_data.platform_id,
            )
            .first()
        )
        if not integration:
            raise HTTPException(
                status_code=400, detail="User is not integrated with this platform"
            )

        credential = CredentialDetail(
            user_id=credential_data.user_id,
            platform_id=credential_data.platform_id,
            integration_id=integration.id,
            key=credential_data.key,
            value=credential_data.value,
        )
        self.db.add(credential)
        self.db.commit()

        return credential
