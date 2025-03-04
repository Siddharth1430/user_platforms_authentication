from pydantic import BaseModel
from typing import Optional, List


class UserSchema(BaseModel):
    username: str
    password: str
    is_admin: bool = False


class UserResponseSchema(BaseModel):
    id: int
    username: str
    is_admin: bool


class PlatformSchema(BaseModel):
    name: str
    description: Optional[str] = None


class PlatformResponseSchema(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class UserIntegrationSchema(BaseModel):
    # user_id: int
    platform_id: int
    is_active: bool


class AdminIntegrationSchema(BaseModel):
    user_id: int
    platform_id: int
    is_active: bool


class AdminCredentialDetailSchema(BaseModel):
    user_id: int
    platform_id: int

    key: str
    value: str


class CredentialDetailSchema(BaseModel):
    # user_id: int
    platform_id: int

    key: str
    value: str


class CredentialIntegration(BaseModel):
    integration_data: UserIntegrationSchema
    credentials: List[CredentialDetailSchema]


class UserIntegrationResponseSchema(BaseModel):
    id: int
    user_id: int
    platform_id: int
    is_active: bool
    user: UserResponseSchema
    platform: PlatformResponseSchema


class CredentialDetailResponseSchema(BaseModel):
    id: int
    user_id: int
    platform_id: int
    key: str
    # value: str
    user: UserResponseSchema
    platform: PlatformResponseSchema


class CurrentUserResponseSchema(BaseModel):
    username: str
    platforms: List[PlatformResponseSchema]


class UserIntegrationWithDetailsSchema(BaseModel):
    id: int
    platform: PlatformResponseSchema
    details: List[CredentialDetailSchema]
