from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr

from . import ModelBase


class UserAccount(ModelBase):
    user_id: int
    server_id: int
    server_user_id: int
    server_user_name: str
    checked_at: int


class UserBase(schemas.BaseUser):
    username: str
    country: str


class UserRead(UserBase):
    privileges: int
    created_at: datetime
    updated_at: datetime


class UserFull(UserRead):
    accounts: list[UserAccount]


class UserUpdate(ModelBase):
    password: Optional[str]
    email: Optional[EmailStr]
    nickname: Optional[str]
    country: Optional[str]
    updated_at: Optional[datetime]
