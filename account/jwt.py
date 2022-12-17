import os

from datetime import datetime, timedelta
from typing import Dict, Union, Any, Optional
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv
load_dotenv('.env')

from core.settings import settings


"""constants for creating access and refresh tokens"""


ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES
ALGORITHM = settings.ALGORITHM
JWT_ACCESS_SECRET_KEY = settings.JWT_ACCESS_SECRET_KEY
JWT_REFRESH_SECRET_KEY = settings.JWT_REFRESH_SECRET_KEY


"""function to hash user passwords"""

pass_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:

    def verify_password(self, plain_password: str, hashed_password: str):
        res = pass_context.verify(plain_password, hashed_password)
        return res

    def get_password_hash(self, password: str):
        return pass_context.hash(password)


hasher = Hasher()


"""functions for generating access and refresh tokens"""


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_ACCESS_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token):
    decoded_jwt = jwt.decode(token.credentials, JWT_ACCESS_SECRET_KEY, algorithms=[ALGORITHM])
    user = decoded_jwt.get("sub").replace("email=", "").replace("password=", "").replace("'", "").split()
    return user


