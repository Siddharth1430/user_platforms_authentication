from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.database.models import Platform, User
from typing import List, Optional
from app.filters.filter import PlatformFilter


class PlatformService:
    def __init__(self, db: Session):
        self.db = db

    def get_platform_by_id(self, platform_id: int):
        """
        Retrieves a platform by its id
        """
        return self.db.query(Platform).filter(Platform.id == platform_id).first()

    def get_user_platforms(self, user_id: int, filters: PlatformFilter):
        """
        Fetches platforms associated with a specific user, with optional filters
        """
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        query = self.db.query(Platform).filter(Platform.users.contains(user))
        query = filters.filter(query)
        result = self.db.execute(query)
        return result.scalars().all()
        # result = self.db.execute(query)

        # return result
