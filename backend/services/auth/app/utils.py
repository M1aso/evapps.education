import os
import uuid
from datetime import datetime, timedelta
from passlib.hash import bcrypt
import jwt
from .config import settings


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.verify(password, hashed)


def create_access_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": datetime.utcnow() + timedelta(seconds=settings.access_token_ttl),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")


def create_refresh_token() -> str:
    return uuid.uuid4().hex + uuid.uuid4().hex
