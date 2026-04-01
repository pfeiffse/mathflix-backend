from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from core.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def create_access_token(user_id: int, role: str):
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_EXPIRE_MIN
    )
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)


def create_refresh_token(user_id: int):
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_EXPIRE_DAYS
    )
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": expire
    }
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGO)