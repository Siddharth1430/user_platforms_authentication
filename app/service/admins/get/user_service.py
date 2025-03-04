from sqlalchemy.orm import Session
from app.database.models import User
from typing import List, Optional
from app.filters.filter import UserFilter


class UserService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self, filters: UserFilter):
        """
        Retrieves a list of users from the database with optional filtering
        """
        query = self.db.query(User)
        query = filters.filter(query)
        result = self.db.execute(query)
        return list(result.scalars().all())
        # result = self.db.execute(query)

        # return list(result.scalars())

    def get_user_by_id(self, user_id: int):
        """
        Fetches a single user by their id
        """
        return self.db.query(User).filter(User.id == user_id).first()
