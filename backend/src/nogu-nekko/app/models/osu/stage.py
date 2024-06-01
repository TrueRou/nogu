import datetime
from typing import TYPE_CHECKING
from sqlmodel import Field, Relationship, SQLModel, Session, select
from app.constants.exceptions import glob_not_belongings, glob_no_permission

from app.constants.osu import Mods, Ruleset, WinCondition

if TYPE_CHECKING:
    from ..ast_condition import AstCondition
    from ..user import User
    from ..team import TeamUserLink, TeamRole


class StageBase(SQLModel):
    name: str = Field(index=True)
    description: str | None
    ruleset: Ruleset
    win_condition: WinCondition

    team_id: int = Field(foreign_key="teams.id")
    playlist_id: int | None = Field(foreign_key="osu_playlists.id")


class StageUpdate(SQLModel):
    name: str | None
    description: str | None
    win_condition: WinCondition | None


class Stage(StageBase, table=True):
    __tablename__ = "osu_stages"

    id: int | None = Field(default=None, primary_key=True)
    version: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.now(datetime.UTC))
    updated_at: datetime.datetime  # we have to mannually update this column


class StageMapBase(SQLModel):
    stage_id: int = Field(foreign_key="osu_stages.id", primary_key=True)
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

    condition: AstCondition = Relationship()


class StageSrv:
    def check_belongings(session: Session, stage: Stage, user: User):
        if stage and user:
            sentence = select(TeamUserLink).where(TeamUserLink.team_id == stage.team_id, TeamUserLink.user_id == user.id)
            if session.exec(sentence).first() is None:
                raise glob_not_belongings

    def check_permission(session: Session, stage: Stage, user: User, permission: TeamRole):
        if stage and user:
            sentence = select(TeamUserLink).where(
                TeamUserLink.team_id == stage.team_id, TeamUserLink.user_id == user.id, TeamUserLink.role <= permission
            )
            if session.exec(sentence).first() is None:
                raise glob_no_permission
