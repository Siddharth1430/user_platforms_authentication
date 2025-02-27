from pydantic import BaseModel
from typing import Optional


class UserSchema(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserResponseSchema(BaseModel):
    id: int
    username: str
    password: str
    is_admin: bool


class PlatformResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class CredentialResponseSchema(BaseModel):
    user_id: int
    platform_id: int
