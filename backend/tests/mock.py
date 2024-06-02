from polyfactory.factories.sqlalchemy_factory import SQLAlchemyFactory
from polyfactory import Ignore

from nogu.app.models.team import Team
from nogu.app.models.user import User


class TeamFactory(SQLAlchemyFactory[Team]): ...


class UserFactory(SQLAlchemyFactory[User]):
    active_team_id = Ignore()
