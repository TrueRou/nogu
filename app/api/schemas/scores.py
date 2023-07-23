from datetime import datetime

from app.api.schemas import ModelBase
from app.api.schemas.beatmaps import BeatmapBase
from app.constants.servers import Server


class ScoreBase(ModelBase):
    user_id: int
    beatmap_md5: str
    score: int
    accuracy: float
    highest_combo: int
    full_combo: bool
    mods: int
    num_300s: int
    num_100s: int
    num_50s: int
    num_misses: int
    num_gekis: int
    num_katus: int
    grade: str
    mode: int
    server_id: int

    @staticmethod
    def from_abs(beatmap_md5: str, user_id: int, keywords: str, max_combo: int, mods: int, mode: int) -> 'ScoreBase':
        data = keywords.split()
        # 5miss 96.5acc 600c 100w
        miss = 0
        acc = 100.0
        combo = max_combo
        score = 1000000
        for item in data:
            if item.endswith("miss"):
                miss = int(item[:-4])
            elif item.endswith("acc"):
                acc = float(item[:-3])
            elif item.endswith("c"):
                combo = int(item[:-1])
            elif item.endswith("w"):
                score = float(item[:-1]) * 10000.0
        n300 = max_combo - miss
        numerator = (acc * 300 * (miss + n300)) - (300 * n300)
        denominator = 100 - acc
        n100 = numerator / denominator
        full_combo = miss == 0
        return ScoreBase(user_id=user_id, beatmap_md5=beatmap_md5, score=score, accuracy=acc, highest_combo=combo,
                         full_combo=full_combo, mods=mods, num_300s=n300, num_100s=n100, num_misses=miss, num_gekis=0,
                         num_katus=0, mode=mode, server_id=Server.LOCAL, grade='R')


class ScoreRead(ScoreBase):
    performance_points: float
    created_at: datetime
    stage_id: int
    beatmap: BeatmapBase
