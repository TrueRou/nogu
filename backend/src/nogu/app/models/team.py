import datetime
from enum import IntEnum, auto
from sqlmodel import Field, Relationship, SQLModel, Session, select

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
    def check_belongings(session: Session, team: Team, user: User) -> bool:
        if team and user:
            sentence = select(TeamUserLink).where(TeamUserLink.team_id == team.id, TeamUserLink.user_id == user.id)
            return session.exec(sentence).first() is not None
