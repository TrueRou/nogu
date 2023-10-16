from datetime import datetime

from app.api.schemas import ModelBase, convert_to_optional


class StageBase(ModelBase):
    name: str
    mode: int
    formula: int
    pool_id: int
    team_id: int


class StageRead(StageBase):
    id: int
    created_at: datetime
    updated_at: datetime


class StageMapBase(ModelBase):
    map_md5: str
    description: str
    condition_ast: str
    condition_name: str
    condition_represent_mods: int


class StageMapRead(StageMapBase):
    stage_id: int


class StageUpdate(ModelBase):
    __annotations__ = convert_to_optional(StageBase)
