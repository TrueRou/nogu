from datetime import datetime

from app.api.schemas import ModelBase, convert_to_optional


class StageBase(ModelBase):
    id: int
    name: str
    mode: int
    formula: int
    pool_id: int
    team_id: int


class StageRead(StageBase):
    created_at: datetime
    updated_at: datetime


class StageUpdate(ModelBase):
    __annotations__ = convert_to_optional(StageBase)
