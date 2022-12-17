from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class BaseUser(BaseModel):
    email: EmailStr


class UserCreate(BaseUser):
    password: str = Field(min_length=6, max_length=14)

    class Config:
        orm_mode = True


class UserResponse(BaseUser):
    id: int

    class Config:
        orm_mode = True


class SuperUserResponse(UserResponse):
    is_superuser: bool


class User(BaseUser):
    is_active: bool | None = None
    is_superuser: bool | None = None


class TokenData(BaseModel):
    email: Optional[str] = None
    expires: datetime


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str