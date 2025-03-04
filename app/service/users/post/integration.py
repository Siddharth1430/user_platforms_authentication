from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.models import User, CredentialDetail, UserIntegration, Platform
from app.database.schemas import CredentialIntegration


class IntegrationServices:
    def __init__(
        self,
        db: Session,
        integrate_cred: CredentialIntegration,
        user,
    ):
        self.db = db
        self.integrate_cred = integrate_cred
        self.user = user

    def integrate(self):
        """
        Establishes an integration between an user and platform
        """
        existing_user = self.db.query(User).filter(User.id == self.user.id).first()
        existing_platform = (
            self.db.query(Platform)
            .filter(Platform.id == self.integrate_cred.integration_data.platform_id)
            .first()
        )
        if not existing_user or not existing_platform:
            raise HTTPException(status_code=404, detail="User or Platform not found")

        integration = (
            self.db.query(UserIntegration)
            .filter(
                UserIntegration.user_id == self.user.id,
                UserIntegration.platform_id
                == self.integrate_cred.integration_data.platform_id,
            )
            .first()
        )

        if not integration:
            integration = UserIntegration(
                user_id=self.user.id,
                platform_id=self.integrate_cred.integration_data.platform_id,
                is_active=self.integrate_cred.integration_data.is_active,
            )
            self.db.add(integration)
            self.db.flush()

        for cred in self.integrate_cred.credentials:
            credential = CredentialDetail(
                user_id=self.user.id,
                platform_id=cred.platform_id,
                integration_id=integration.id,
                key=cred.key,
                value=cred.value,
            )
            self.db.add(credential)

        self.db.commit()

        return integration
