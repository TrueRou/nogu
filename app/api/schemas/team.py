from datetime import datetime
from typing import Optional

from app.api.schemas import ModelBase
from app.api.schemas.stage import StageRead


class TeamBase(ModelBase):
    name: str
    privacy: int
    achieved: bool
    finish_at: Optional[datetime]
    active_stage_id: Optional[int]


class TeamRead(ModelBase):
    id: int
    name: str
    privacy: int
    achieved: bool
    create_at: datetime
    finish_at: Optional[datetime]
    active_stage: Optional[StageRead]
