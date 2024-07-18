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
