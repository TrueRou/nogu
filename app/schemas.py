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


class Pool(ModelBase):
    id: int
    name: str
    mode_int: int
    description: str
    privacy: int
    creation_time: datetime
    last_updated: datetime
    owner_id: int


class Stage(ModelBase):
    id: int
    name: str
    mode_int: int
    creation_time: datetime
    last_updated: datetime
    pool_id: int
    team_id: int


class Beatmap(ModelBase):
    md5: str
    # beatmap fields
    set_id: int
    id: int
    status: str
    total_length: int
    user_id: int
    version: str
    accuracy: float
    ar: float
    cs: float
    hp: float
    od: float
    bpm: float
    convert: bool
    count_circles: int
    count_sliders: int
    count_spinners: int
    hit_length: int
    last_updated: datetime
    mode_int: int
    max_combo: int


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


class ScoreFull(ScoreBase):
    server_id: int
    stage: Stage
    beatmap: Beatmap
