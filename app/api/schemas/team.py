from datetime import datetime
from typing import Optional

from app.api.schemas import ModelBase, convert_to_optional
from app.api.schemas.stage import StageRead


class TeamBase(ModelBase):
    name: str
    privacy: int
    achieved: bool
    finish_at: Optional[datetime]
    active_stage_id: Optional[int]


class TeamRead(TeamBase):
    id: int
    create_at: datetime
    active_stage: Optional[StageRead]


class TeamUpdate(ModelBase):
    __annotations__ = convert_to_optional(TeamBase)
