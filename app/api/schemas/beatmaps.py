from datetime import datetime

from app.api.schemas import ModelBase
from app.constants import tasks
from app.interaction import User


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


class QueuedBeatmaps(ModelBase):
    results: list[BeatmapBase]
    failures: list[str]

    @staticmethod
    async def generate_now(user: User):
        return QueuedBeatmaps(
            results=await tasks.beatmap_results[user.id].get(),
            failures=await tasks.beatmap_failures[user.id].get()
        )
