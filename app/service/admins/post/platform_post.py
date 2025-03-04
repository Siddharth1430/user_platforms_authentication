from sqlalchemy.orm import Session
from app.database.models import Platform
from app.database.schemas import PlatformSchema


class PlatformPostService:
    def __init__(self, db: Session):
        self.db = db

    def create_platform(self, platform_data: PlatformSchema):
        """
        Creates a new platform entry in the database
        """
        platform = Platform(
            name=platform_data.name, descripition=platform_data.description
        )
        self.db.add(platform)
        self.db.commit()
        return platform
