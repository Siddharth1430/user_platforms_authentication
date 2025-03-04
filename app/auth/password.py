from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str):
    """
    Hashes a password using bcrypt
    """
    return pwd_context.hash(password)


def verify_password(hashed_password: str, plain_password: str):
    """
    Verfies if a password matches its hash
    """
    return pwd_context.verify(hashed_password, plain_password)
