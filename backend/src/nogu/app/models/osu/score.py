import datetime
from nogu.app import database
from nogu.app.models.osu.beatmap import Beatmap, BeatmapSrv
from nogu.app.objects import AstChecker
from sqlmodel import Field, Relationship, SQLModel, Session, select
from ossapi.models import Score as BanchoScore

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
    beatmap_md5: str = Field(index=True, foreign_key="osu_beatmaps.md5")


class Score(ScoreBase, table=True):
    __tablename__ = "osu_scores"

    id: int | None = Field(default=None, primary_key=True)
    full_combo: bool
    grade: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    user_id: int = Field(index=True, foreign_key="users.id")
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

    def _check_ast(score: Score, stage_map: StageMap) -> bool:
        variables = {
            "acc": score.accuracy,
            "max_combo": score.highest_combo,
            "mods": score.mods,
            "score": score.score,
        }
        return AstChecker(stage_map.condition.ast_expression).check(variables)

    def _ensure_grade(score: Score, beatmap: Beatmap):
        score.grade = "S"
        score.full_combo = True

    def submit_score(session: Session, score: ScoreBase, user: User):
        beatmap = session.get(Beatmap, score.beatmap_md5)
        if beatmap is None:
            beatmap = BeatmapSrv.request_api(session, score.beatmap_md5)
        # if the beatmap is not found, we can still continue submitting the score
        prebuild_score = Score(**score.model_dump(), user_id=user.id)
        ScoreSrv._ensure_grade(prebuild_score, beatmap)

        # find the stage that the score belongs to
        sentence = (
            select(StageMap, Stage, Team, Beatmap)
            .join(Stage, onclause=StageMap.stage_id == Stage.id)
            .join(Team, onclause=Stage.team_id == Team.id)
            .join(TeamUserLink, onclause=TeamUserLink.team_id == Team.id)
            .join(Beatmap, onclause=StageMap.map_md5 == Beatmap.md5)
            .where(StageMap.map_md5 == score.beatmap_md5)
            .where(Team.active == True)
            .where(TeamUserLink.user_id == user.id, TeamUserLink.team_id == Team.id)
            .order_by(Team.updated_at)
        )
        matched = session.exec(sentence).first()
        if matched and ScoreSrv._check_ast(prebuild_score, matched[0]):
            prebuild_score.stage_id = matched[1].id

        database.add_model(session, prebuild_score)
        return prebuild_score

    def submit_partial(session: Session, keywords: str, beatmap_md5: str, user: User):
        sentence = (
            select(StageMap, Beatmap, Stage)
            .join(Stage, onclause=StageMap.stage_id == Stage.id)
            .join(Beatmap, onclause=StageMap.map_md5 == Beatmap.md5)
            .join(Team, onclause=Stage.team_id == Team.id)
            .join(TeamUserLink, onclause=TeamUserLink.team_id == Team.id)
            .where(StageMap.map_md5 == beatmap_md5)
            .where(Team.active == True)
            .where(TeamUserLink.user_id == user.id, TeamUserLink.team_id == Team.id)
            .order_by(Team.updated_at)
        )

        matched = session.exec(sentence).first()
        if matched:
            (stage_map, beatmap, stage) = matched
            data = keywords.split()  # 5miss 96.5acc 600c 100w
            miss = 0
            acc = 100.0
            combo = beatmap.max_combo
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
            n300 = beatmap.max_combo - miss
            numerator = (acc * 300 * (miss + n300)) - (300 * n300)
            denominator = 100 - acc
            n100 = numerator / denominator

            fake_score = Score(
                score=score,
                accuracy=acc,
                highest_combo=combo,
                mods=stage_map.represent_mods,
                num_300s=n300,
                num_100s=n100,
                num_misses=miss,
                num_gekis=0,
                num_katus=0,
                num_50s=0,
                ruleset=stage.ruleset,
                osu_server=Server.LOCAL,
                beatmap_md5=beatmap_md5,
                user_id=user.id,
                stage_id=stage.id,
            )
            ScoreSrv._ensure_grade(fake_score, beatmap)
            if ScoreSrv._check_ast(fake_score, stage_map):
                database.add_model(session, fake_score)
        return fake_score

    def submit_inspected(session: Session, score: BanchoScore, user: User):
        if isinstance(score, BanchoScore):
            score = ScoreBase(
                score=score.score,
                accuracy=score.accuracy,
                highest_combo=score.max_combo,
                mods=score.mods.value,
                num_300s=score.statistics.count_300,
                num_100s=score.statistics.count_100,
                num_50s=score.statistics.count_50,
                num_misses=score.statistics.count_miss,
                num_gekis=score.statistics.count_geki,
                num_katus=score.statistics.count_katu,
                ruleset=score.mode_int,
                osu_server=Server.BANCHO,
                beatmap_md5=score.beatmap.checksum,
            )
            return ScoreSrv.submit_score(session, score, user)
