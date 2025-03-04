from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.database.models import CredentialDetail
from app.database.schemas import CredentialDetailSchema


class CredentialServices:
    def __init__(self, db: Session, user, credential_data: CredentialDetailSchema):
        self.db = db
        self.user = user
        self.credential_data = credential_data

    def cred_service(self):
        """
        Adds a new credential for a user's platform integration
        """
        integration = (
            self.db.query(CredentialDetail)
            .filter(
                CredentialDetail.user_id == self.user.id,
                CredentialDetail.platform_id == self.credential_data.platform_id,
            )
            .first()
        )

        if not integration:
            raise HTTPException(status_code=404, detail="Integration not found")

        credential = CredentialDetail(
            user_id=self.user.id,
            platform_id=self.credential_data.platform_id,
            integration_id=integration.id,
            key=self.credential_data.key,
            value=self.credential_data.value,
        )

        self.db.add(credential)
        self.db.commit()

        return credential
