import datetime
from fastapi import Depends, status
from fastapi.security import SecurityScopes
from nogu.app.database import require_session
from sqlmodel import Field, Relationship, SQLModel, Session
from nogu.app.constants.exceptions import APIException

from nogu.app.constants.osu import Mods, Ruleset, WinCondition
from ..ast_condition import AstCondition
from ..user import User, UserSrv
from ..team import TeamSrv


class StageBase(SQLModel):
    name: str = Field(index=True)
    description: str | None
    ruleset: Ruleset
    win_condition: WinCondition

    playlist_id: int | None = Field(foreign_key="osu_playlists.id")


class StageUpdate(SQLModel):
    name: str | None
    description: str | None
    win_condition: WinCondition | None


class Stage(StageBase, table=True):
    __tablename__ = "osu_stages"

    id: int | None = Field(default=None, primary_key=True)
    version: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)  # we have to mannually update this column

    team_id: int = Field(foreign_key="teams.id")


class StageMapBase(SQLModel):
    map_md5: str = Field(foreign_key="osu_beatmaps.md5", primary_key=True)
    label: str  # NM1
    description: str | None  # Consistency jumps
    represent_mods: Mods  # HDDTRX

    condition_id: int = Field(foreign_key="ast_conditions.id")


class StageMapUpdate(SQLModel):
    label: str | None
    description: str | None
    represent_mods: Mods | None
    condition_id: int | None


class StageMap(StageMapBase, table=True):
    __tablename__ = "osu_stage_maps"

    stage_id: int = Field(foreign_key="osu_stages.id", primary_key=True)
    condition: AstCondition = Relationship()


class StageSrv:
    # scope: access, access-sensitive, member, admin, owner
    def require_stage(
        security: SecurityScopes, stage_id: int, session: Session = Depends(require_session), user: User = Depends(UserSrv.require_user_optional)
    ):
        stage = session.get(Stage, stage_id)
        if stage is None:
            raise APIException("Stage not found", "stage.not-found", status.HTTP_404_NOT_FOUND)
        TeamSrv.require_team(security, stage.team_id, user)  # check if user have proper grant to the team
        return stage
