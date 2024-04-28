from datetime import datetime

from app.api.schemas import ModelBase, convert_to_optional


class StageBase(ModelBase):
    name: str
    mode: int
    formula_set: int
    playlist_id: int
    team_id: int


class StageRead(StageBase):
    id: int
    version: int
    created_at: datetime
    updated_at: datetime


class StageMapBase(ModelBase):
    map_md5: str
    label: str
    description: str
    represent_mods: int
    condition_ast: str
    condition_name: str
    


class StageMapRead(StageMapBase):
    stage_id: int


class StageUpdate(ModelBase):
    __annotations__ = convert_to_optional(StageBase)
