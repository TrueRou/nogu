import datetime
from enum import IntEnum, auto
from fastapi import Depends
from fastapi.security import SecurityScopes
from nogu.app.constants.exceptions import APIException
from nogu.app.database import manual_session
from sqlmodel import Field, Relationship, SQLModel, Session, select
from nogu.app.api.users import require_user_optional

from .user import User, UserRead


class TeamVisibility(IntEnum):
    PUBLIC = auto()
    PROTECTED = auto()
    PRIVATE = auto()


class TeamRole(IntEnum):
    OWNER = auto()
    ADMIN = auto()
    MEMBER = auto()


class TeamBase(SQLModel):
    name: str = Field(index=True)
    slogan: str | None
    visibility: TeamVisibility = Field(default=TeamVisibility.PROTECTED)
    active_until: datetime.datetime | None  # null if team is active indefinitely


# for sqlmodel to serialize the full team
class TeamRead(TeamBase):
    id: int
    active: bool
    created_at: datetime.datetime
    updated_at: datetime.datetime


class TeamUpdate(SQLModel):
    name: str | None
    slogan: str | None
    visibility: TeamVisibility | None
    active: bool | None
    active_until: datetime.datetime | None


class Team(TeamBase, table=True):
    __tablename__ = "teams"

    id: int | None = Field(default=None, primary_key=True)
    active: bool = Field(default=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)  # we have to mannually update this column

    user_links: list["TeamUserLink"] = Relationship(sa_relationship_kwargs={"lazy": "subquery"})


class TeamUserLink(SQLModel, table=True):
    __tablename__ = "team_user_links"

    team_id: int | None = Field(default=None, foreign_key="teams.id", primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", primary_key=True)
    role: TeamRole = Field(default=TeamRole.MEMBER)
    joined_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)  # we have to mannually update this column

    user: User = Relationship(sa_relationship_kwargs={"lazy": "subquery"})


class TeamWithMembers(TeamRead):
    class TeamUserLinkPublic(SQLModel):
        role: TeamRole
        user: UserRead

    user_links: list[TeamUserLinkPublic]


class TeamSrv:
    def _ensure_privilege(session: Session, team: Team, user: User | None, role: TeamRole = None) -> tuple[bool, APIException]:
        if user is None:
            return False, APIException("Login is required to access that team.", "team.login-required", 40310)
        sentence = select(TeamUserLink).where(TeamUserLink.team_id == team.id, TeamUserLink.user_id == user.id)
        if role is not None:
            sentence = sentence.where(TeamUserLink.role <= role)
        if session.exec(sentence).first() is None:
            return False, APIException("You have no privilege to do that.", "team.not-priv", 40311)
        return True, None

    def _ensure_privilege_throw(session: Session, team: Team, user: User | None, role: TeamRole = None):
        result, exception = TeamSrv._ensure_privilege(session, team, user, role)
        if not result:
            raise exception

    # scope: access, access-sensitive, member, admin, owner
    def get_team(security: SecurityScopes, team_id: int, user: User = Depends(require_user_optional)):
        with manual_session() as session:
            team = session.get(Team, team_id)
            if team is None:
                raise APIException("Team not found", "team.not-found", 40410)

            if "access" in security.scopes or security.scopes == []:
                if team.visibility == TeamVisibility.PRIVATE:
                    TeamSrv._ensure_privilege_throw(session, team, user)

            if "access-sensitive" in security.scopes:
                if team.visibility >= TeamVisibility.PROTECTED:
                    TeamSrv._ensure_privilege_throw(session, team, user)

            if "member" in security.scopes:
                TeamSrv._ensure_privilege_throw(session, team, user)

            if "admin" in security.scopes:
                TeamSrv._ensure_privilege_throw(session, team, user, TeamRole.ADMIN)

            if "owner" in security.scopes:
                TeamSrv._ensure_privilege_throw(session, team, user, TeamRole.OWNER)

            return team
