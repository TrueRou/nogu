import datetime
from typing import TYPE_CHECKING
from nogu.app import database
from nogu.app.objects import AstChecker
from sqlmodel import Field, Relationship, SQLModel, Session, select

from nogu.app.constants.osu import Server, Mods, Ruleset
from .performance import Performance
from ..user import User
from ..team import TeamUserLink, Team, TeamVisibility
from .stage import Stage, StageMap


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
    beatmap_md5: str = Field(index=True, foreign_key="osu_beatmaps.md5")


class Score(ScoreBase, table=True):
    __tablename__ = "osu_scores"

    id: int | None = Field(default=None, primary_key=True)
    full_combo: bool
    grade: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    stage_id: int | None = Field(index=True, foreign_key="osu_stages.id")
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

    def submit_score(session: Session, score: ScoreBase, user: User):
        variables = {
            "acc": score.accuracy,
            "max_combo": score.highest_combo,
            "mods": score.mods,
            "score": score.score,
        }
        # find the stage that the score belongs to
        sentence = (
            select(StageMap, Stage, Team)
            .join(Stage, onclause=StageMap.stage_id == Stage.id)
            .join(Team, onclause=Stage.team_id == Team.id)
            .join(TeamUserLink, onclause=TeamUserLink.team_id == Team.id)
            .where(StageMap.map_md5 == score.beatmap_md5)
            .where(Team.active == True)
            .where(TeamUserLink.user_id == user.id, TeamUserLink.team_id == Team.id)
            .order_by(Team.updated_at)
        )
        matched = session.exec(sentence).first()
        prebuild_score = Score(**score.model_dump(), full_combo=True, grade="S")
        if matched and AstChecker(matched[0].condition.ast_expression).check(variables):
            prebuild_score.stage_id = matched[1].id
        database.add_model(session, prebuild_score)
        return prebuild_score
