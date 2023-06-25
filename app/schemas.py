from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel


def convert_to_optional(schema):
    return {k: Optional[v] for k, v in schema.__annotations__.items()}


class ModelBase(BaseModel):
    class Config:
        orm_mode = True


class UserAccount(BaseModel):
    user_id: int
    server_id: int
    server_user_id: int
    server_user_name: str
    last_check_time: int


class UserFull(schemas.BaseUser):
    nickname: str
    privilege: int
    creation_time: datetime
    accounts: list[UserAccount]


class UserCreate(schemas.BaseUserCreate):
    nickname: str


class UserUpdate(schemas.BaseUserUpdate):
    nickname: Optional[str]


class ScoreBase(ModelBase):
    accuracy: float
    created_at: int
    max_combo: int
    mode_int: int
    mods: int
    rank: str
    score: int
    count_300: int
    count_100: int
    count_50: int
    count_miss: int
    map_md5: str


class ScoreCreate(ScoreBase):
    server_id: int
