import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Session, select

from app.constants.osu import Server, Mods, Ruleset
from app.constants.exceptions import glob_not_belongings
from .performance import Performance
from ..user import User

if TYPE_CHECKING:
    from .stage import Stage, StageMap
    from ..team import TeamUserLink, Team


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
    # you have permission to fetch the beatmap scores in your team stages.
    def check_score_belongings(session: Session, score: Score, user: User):
        if score is None or score.user_id == user.id:
            return  # You can fetch your own scores.
        # find if the score is made by a teammate in your teams.
        sentence = select(User, Team).join(Team).join(TeamUserLink).where(TeamUserLink.user_id == user.id, User.id == score.user_id)
        (mate, team) = session.exec(sentence).first()
        if mate and team:
            # it is a score made by a teammate in your team, let's check if the beatmap is in that team stages.
            sentence = select(StageMap).join(Stage).where(Stage.team_id == team.id, StageMap.map_md5 == score.beatmap_md5)
            if session.exec(sentence).first():
                # the beatmap is in the team stages, you can fetch the score.
                return
        raise glob_not_belongings
