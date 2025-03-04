from sqlalchemy.orm import Session
from typing import List
from app.database.models import User, Platform
from app.database.schemas import PlatformResponseSchema
from app.filters.filter import PlatformFilter


class PlatformGetServices:
    def __init__(self, db: Session):
        self.db = db

    def get_user_platforms(self, current_user: User, filters: PlatformFilter):
        """
        Fetch platforms that the current user is integrated with.
        """
        query = self.db.query(Platform).filter(Platform.users.contains(current_user))
        query = filters.filter(query)
        result = self.db.execute(query)
        return result.scalars().all()
