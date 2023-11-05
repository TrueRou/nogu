from datetime import datetime
from typing import Optional

from fastapi_users.schemas import CreateUpdateDictModel
from pydantic import EmailStr

from . import ModelBase


class UserAccount(ModelBase):
    user_id: int
    server_id: int
    server_user_id: int
    server_user_name: str
    checked_at: datetime


class UserBase(ModelBase):
    email: EmailStr
    username: str
    country: str


class UserWrite(UserBase, CreateUpdateDictModel):
    password: str


# for simple display of user
class UserSimple(ModelBase):
    id: int
    username: str
    country: str
    privileges: int


class UserRead(UserBase):
    id: int
    privileges: int
    created_at: datetime
    updated_at: datetime
    accounts: list[UserAccount]


class UserUpdate(ModelBase):
    password: Optional[str]
    email: Optional[EmailStr]
    nickname: Optional[str]
    country: Optional[str]
    updated_at: Optional[datetime]
