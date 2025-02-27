from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Association table for Many-to-Many connection between table users and platforms
user_platform = Table(
    "user_platform",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("platform_id", Integer, ForeignKey("platforms.id"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    # The is_admin column will check if the user is an admin or not
    is_admin = Column(Boolean, default=False)

    # Many-to-Many relationship with table platforms
    platforms = relationship(
        "Platform", secondary=user_platform, back_populates="users"
    )
    # One-to-Many relationship with table credentials
    credentials = relationship("Credential", back_populates="user")


class Platform(Base):
    __tablename__ = "platforms"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)

    # Many-to-Many relationship with table users
    users = relationship("User", secondary=user_platform, back_populates="platforms")
    # One-to-Many relationship with table credentials
    credentials = relationship("Credential", back_populates="platform")


class Credential(Base):
    __tablename__ = "credentials"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    platform_id = Column(Integer, ForeignKey("platforms.id"), nullable=False)

    # Many-to-One relationship with table users
    user = relationship("User", back_populates="credentials")
    # Many-to-One relationship with table platforms
    platform = relationship("Platform", back_populates="credentials")

    details = relationship(
        "CredentialDetail", back_populates="credential", cascade="all,delete-orphan"
    )


class CredentialDetail(Base):
    __tablename__ = "credential_details"

    id = Column(Integer, primary_key=True)
    credential_id = Column(Integer, ForeignKey("credentials.id"), nullable=False)
    key = Column(String, nullable=False)
    value = Column(String, nullable=False)

    credential = relationship("Credential", back_populates="details")
