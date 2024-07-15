from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory.factories.pydantic_factory import ModelFactory
from polyfactory import Ignore

from nogu.app.models.ast_condition import AstCondition
from nogu.app.models.osu.beatmap import Beatmap
from nogu.app.models.osu.score import Score, ScoreBase
from nogu.app.models.osu.stage import Stage, StageMap
from nogu.app.models.team import Team
from nogu.app.models.user import User


class TeamFactory(SQLAlchemyFactory[Team]): ...


class StageFactory(SQLAlchemyFactory[Stage]):
    team_id = Ignore()
    playlist_id = Ignore()
    analysis = Ignore()


class UserFactory(SQLAlchemyFactory[User]):
    active_team_id = Ignore()


class ScoreFactory(SQLAlchemyFactory[Score]):
    user_id = Ignore()
    stage_id = Ignore()
    beatmap_md5 = Ignore()
    analysis = Ignore()


class ScoreBaseFactory(ModelFactory[ScoreBase]):
    user_id = Ignore()
    stage_id = Ignore()
    beatmap_md5 = Ignore()


class BeatmapFactory(SQLAlchemyFactory[Beatmap]):
    uploaded_by = Ignore()


class StageMapFactory(SQLAlchemyFactory[StageMap]):
    stage_id = Ignore()
    map_md5 = Ignore()
    condition_id = Ignore()
    analysis = Ignore()


class AstConditionFactory(SQLAlchemyFactory[AstCondition]):
    user_id = Ignore()
