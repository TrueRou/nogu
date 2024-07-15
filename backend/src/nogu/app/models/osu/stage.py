import datetime
from fastapi import Depends, status
from fastapi.security import SecurityScopes
from nogu.app.database import require_session
from sqlalchemy import JSON, Column, event
from sqlalchemy.orm import object_session
from sqlmodel import Field, Relationship, SQLModel, Session, select
from nogu.app.constants.exceptions import APIException

from nogu.app.constants.osu import Mods, Ruleset, WinCondition
from ..ast_condition import AstCondition
from ..user import User, UserSrv
from ..team import TeamSrv, TeamUserLink


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
    analysis: dict = Field(sa_column=Column(JSON), default_factory=dict)

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
    analysis: dict = Field(sa_column=Column(JSON), default_factory=dict)


class StageUser(SQLModel, table=True):
    __tablename__ = "osu_stage_users"

    stage_id: int | None = Field(foreign_key="osu_stages.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    analysis: dict = Field(sa_column=Column(JSON), default_factory=dict)


class StageMapUser(SQLModel, table=True):
    __tablename__ = "osu_stage_map_users"

    stage_id: int | None = Field(foreign_key="osu_stages.id", primary_key=True)
    map_md5: str | None = Field(foreign_key="osu_beatmaps.md5", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    analysis: dict = Field(sa_column=Column(JSON), default_factory=dict)


@event.listens_for(TeamUserLink, "after_insert")
def user_after_insert(mapper, connection, team_user_link: TeamUserLink):
    session = object_session(team_user_link)
    stages = session.scalars(select(Stage).where(Stage.team_id == team_user_link.team_id))
    for stage in stages:
        maps = session.scalars(select(StageMap).where(StageMap.stage_id == stage.id))
        session.add(StageUser(stage_id=stage.id, user_id=team_user_link.user_id))
        for map in maps:
            session.add(StageMapUser(stage_id=stage.id, map_md5=map.map_md5, user_id=team_user_link.user_id))
    session.commit()


@event.listens_for(StageMap, "after_insert")
def beatmap_after_insert(mapper, connection, stage_map: StageMap):
    session = object_session(stage_map)
    stage = session.get(Stage, stage_map.stage_id)
    users = session.scalars(select(TeamUserLink).where(TeamUserLink.team_id == stage.team_id))
    for user in users:
        session.add(StageMapUser(stage_id=stage.id, map_md5=stage_map.map_md5, user_id=user.user_id))
    session.commit()


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
