from datetime import datetime
from typing import Optional

from app.api.schemas import ModelBase


class BeatmapBase(ModelBase):
    md5: str
    id: int
    set_id: int
    ranked_status: int
    artist: str
    title: str
    version: str
    creator: str
    filename: str
    total_length: int
    max_combo: int
    mode: int
    bpm: float
    cs: float
    ar: float
    od: float
    hp: float
    star_rating: float
    updated_at: datetime
    server_updated_at: datetime
    server_id: int


class BeatmapEvent(ModelBase):
    status: str
    info: str
    beatmap: Optional[BeatmapBase]
