from jose import jwt
from datetime import datetime, timezone, timedelta
import os
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY", "")
REFRESH_KEY = os.getenv("REFRESH_KEY", "")

# Set the algorithm for jwt
ALGORITHM = "HS256"

# Set the expire time for access token and refresh token
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: dict, expires: timedelta):
    """
    This function will create the access token by using jwt.encode on the data that user gave,
    the SECRET_KEY, and the algorithm(HS256)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(data: dict, expires: timedelta):
    """
    This function will create the refresh token by using jwt.encode on the data that user gave,
    the REFRESH_KEY, and the algorithm(HS256)
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_KEY, algorithm=ALGORITHM)
