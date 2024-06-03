import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Session, select

from nogu.app.constants.osu import Server, Mods, Ruleset
from .performance import Performance
from ..user import User
from ..team import TeamUserLink, Team, TeamVisibility
from .stage import Stage


class ScoreBase(SQLModel):
    score: int
    accuracy: float
    highest_combo: int
    mods: Mods
    num_300s: int
    num_100s: int
    num_50s: int
    num_misses: int
    num_gekis: int
    num_katus: int
    ruleset: Ruleset
    osu_server: int = Field(default=Server.BANCHO)

    user_id: int = Field(index=True, foreign_key="users.id")
    stage_id: int = Field(index=True, foreign_key="osu_stages.id")
    beatmap_md5: str = Field(index=True, foreign_key="osu_beatmaps.md5")


class Score(ScoreBase, table=True):
    __tablename__ = "osu_scores"

    id: int | None = Field(default=None, primary_key=True)
    full_combo: bool
    grade: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    performances: list[Performance] = Relationship()


class ScoreSrv:
    # you have limited permission to fetch the scores.
    def check_score_visibility(session: Session, score: Score, user: User) -> bool:
        # You can fetch your own scores.
        if score is None or score.user_id == user.id:
            return True

        sentence = select(Team).join(Stage).where(Stage.id == score.stage_id)
        team = session.exec(sentence).first()

        assert team is not None  # the stage must belong to a team

        # You can fetch scores that from public teams.
        if team.visibility == TeamVisibility.PUBLIC:
            return True

        # You can fetch scores if you are in the team that the score belongs to.
        sentence = select(TeamUserLink).where(TeamUserLink.team_id == team.id, TeamUserLink.user_id == user.id)
        if session.exec(sentence).first():
            return True

        return False
