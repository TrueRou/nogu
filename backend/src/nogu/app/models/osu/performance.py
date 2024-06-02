from enum import IntEnum, auto
from sqlmodel import Field, SQLModel


class PPFormula(IntEnum):
    BANCHO = auto()


class Performance(SQLModel, table=True):
    __tablename__ = "osu_performances"

    score_id: int = Field(primary_key=True, foreign_key="osu_scores.id")
    formula: PPFormula = Field(default=PPFormula.BANCHO, primary_key=True)
    formula_version: int = Field(default=0)
    performance_points: float
