import datetime
from enum import IntEnum, auto
from fastapi import Depends, status
from fastapi.security import SecurityScopes
from nogu.app.constants.exceptions import APIException
from nogu.app.database import require_session
from nogu.app.utils import ensure_throw
from sqlmodel import Field, Relationship, SQLModel, Session, select

from .user import User, UserRead, UserSrv


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
    def _ensure_role(session: Session, team: Team, user: User | None, role: TeamRole = None) -> tuple[bool, APIException]:
        if user is None:
            return False, APIException("Login is required to access that model.", "model.login-required", status.HTTP_401_UNAUTHORIZED)
        sentence = select(TeamUserLink).where(TeamUserLink.team_id == team.id, TeamUserLink.user_id == user.id)
        if role is not None:
            sentence = sentence.where(TeamUserLink.role <= role.value)
        if session.exec(sentence).first() is None:
            return False, APIException("You have no privilege to do that.", "model.no-priv", status.HTTP_403_FORBIDDEN)
        return True, None

    # scope: access, access-sensitive, member, admin, owner
    def require_team(
        security: SecurityScopes, team_id: int, session: Session = Depends(require_session), user: User = Depends(UserSrv.require_user_optional)
    ):
        team = session.get(Team, team_id)
        if team is None:
            raise APIException("Team not found", "team.not-found", status.HTTP_404_NOT_FOUND)

        if "access" in security.scopes or security.scopes == []:
            if team.visibility == TeamVisibility.PRIVATE:
                ensure_throw(TeamSrv._ensure_role, session, team, user)

        if "access-sensitive" in security.scopes:
            if team.visibility >= TeamVisibility.PROTECTED:
                ensure_throw(TeamSrv._ensure_role, session, team, user)

        if "member" in security.scopes:
            ensure_throw(TeamSrv._ensure_role, session, team, user)

        if "admin" in security.scopes:
            ensure_throw(TeamSrv._ensure_role, session, team, user, TeamRole.ADMIN)

        if "owner" in security.scopes:
            ensure_throw(TeamSrv._ensure_role, session, team, user, TeamRole.OWNER)

        return team
