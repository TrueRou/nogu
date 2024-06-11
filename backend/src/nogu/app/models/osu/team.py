from nogu.app.constants.osu.rulesets import Ruleset
from nogu.app.models.osu.stage import Stage
from nogu.app.models.team import Team, TeamWithMembers
from sqlmodel import Field, Relationship, SQLModel


class OsuTeamDetail(SQLModel):
    ruleset: Ruleset
    team: TeamWithMembers
    stage: Stage
