from sqlalchemy.orm import Session
from app.database.models import UserIntegration
from app.database.schemas import AdminIntegrationSchema


class IntegrationPostService:
    def __init__(self, db: Session):
        self.db = db

    def assign_user(self, integration_data: AdminIntegrationSchema):
        """
        Assigns a user to a platform by creating an integration entry
        """
        integration = UserIntegration(
            user_id=integration_data.user_id, platform_id=integration_data.platform_id
        )
        self.db.add(integration)
        self.db.commit()

        return integration
