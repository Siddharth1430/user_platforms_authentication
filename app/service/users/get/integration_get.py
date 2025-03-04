from sqlalchemy.orm import Session
from app.database.models import UserIntegration, User
from app.database.schemas import UserIntegrationWithDetailsSchema
from app.filters.filter import UserIntegrationFilter


class IntegrationGetServices:
    def __init__(self, db: Session):
        self.db = db

    def get_user_integrations(self, current_user: User, filters: UserIntegrationFilter):
        """
        Fetch user integrations for the current user, including platform details and credentials.
        """
        query = self.db.query(UserIntegration).filter(
            UserIntegration.user_id == current_user.id
        )
        query = filters.filter(query)
        query = filters.sort(query)
        result = self.db.execute(query)
        return result.scalars().all()
