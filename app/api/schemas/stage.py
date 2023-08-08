from datetime import datetime

from app.api.schemas import ModelBase


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
