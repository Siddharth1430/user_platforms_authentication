from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional, List
from app.database.models import Platform, CredentialDetail, CredentialDetail, User


class UserFilter(Filter):
    """
    Defines filtering options for querying users.
    """

    username__ilike: Optional[str]
    is_admin: Optional[bool]
    order_by: Optional[List[str]]

    class Constants(Filter.Constants):
        model = User


class PlatformFilter(Filter):
    """
    Defines filtering options for querying platforms
    """

    name__ilike: Optional[str]
    description__ilike: Optional[str]
    order_by: Optional[List[str]]

    class Constants(Filter.Constants):
        model = Platform


class UserIntegrationFilter(Filter):
    """
    Provides filters for user integrations.
    """

    is_active: Optional[bool]
    order_by: Optional[List[str]]

    class Constants(Filter.Constants):
        model = CredentialDetail


class CredentialDetailFilter(Filter):
    """
    Defines filters for credential details.
    """

    user_id: Optional[int]
    platform_id: Optional[int]
    key: Optional[str]

    class Constants(Filter.Constants):
        model = CredentialDetail
