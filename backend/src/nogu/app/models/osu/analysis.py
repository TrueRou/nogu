from sqlmodel import SQLModel


class ScoreAnalysis(SQLModel):
    completeness: float


class StageMapUserAnalysis(SQLModel):
    play_count: int
    average_accuracy: float
    average_misses: float
    average_score: int
    average_completeness: float


class StageMapAnalysis(SQLModel):
    play_count: int
    average_accuracy: float
    average_misses: float
    average_score: int
    average_completeness: float


class StageUserAnalysis(SQLModel):
    play_count: int
    average_accuracy: float
    average_completeness: float


class StageAnalysis(SQLModel):
    play_count: int


class StageMapSheet(SQLModel):
    map_md5: str
    label: str
    description: str
    title: str
    artist: str
    version: str
    creator: str
    beatmapset_id: int
    beatmap_id: int
    analysis: StageMapAnalysis | None


class StageUserSheet(SQLModel):
    user_id: int
    username: str
    analysis: StageUserAnalysis | None


class StageSheet(SQLModel):
    rows: list[StageUserSheet]
    cols: list[StageMapSheet]
    cells: dict[str, dict[int, StageMapUserAnalysis | None] | None]
