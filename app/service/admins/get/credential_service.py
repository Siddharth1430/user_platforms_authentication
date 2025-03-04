from sqlalchemy.orm import Session
from app.database.models import CredentialDetail
from typing import Optional
from app.filters.filter import CredentialDetailFilter


class CredentialService:
    def __init__(self, db: Session):
        self.db = db

    def get_user_credentials(
        self, user_id: int, platform_id: int, filters: CredentialDetailFilter
    ):
        """
        Retrieves credentials for a specific user on a given platform.
        """
        query = self.db.query(CredentialDetail).filter(
            CredentialDetail.user_id == user_id,
            CredentialDetail.platform_id == platform_id,
        )
        query = filters.filter(query)
        query = filters.sort(query)
        result = self.db.execute(query)
        return result.scalars().all()
