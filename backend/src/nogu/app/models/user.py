import datetime
from enum import IntFlag, auto
from typing import TYPE_CHECKING
from fastapi_users.schemas import CreateUpdateDictModel
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .team import TeamUserLink


class UserPriv(IntFlag):
    UNRESTRICTED = auto()
    ADMIN = auto()


class UserBase(SQLModel):
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True, index=True)
    country: str = Field(default="XX")


# for fastapi-users to create a user
class UserWrite(UserBase, CreateUpdateDictModel):
    password: str


# for fastapi-users to update a user
class UserUpdate(SQLModel):
    password: str | None
    email: str | None
    username: str | None
    country: str | None


# for fastapi-users to read a user
class UserRead(UserBase):
    id: int
    privileges: UserPriv
    created_at: datetime.datetime
    updated_at: datetime.datetime


class User(UserBase, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    privileges: UserPriv = Field(default=UserPriv.UNRESTRICTED)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)

    active_team_id: int | None = Field(foreign_key="teams.id")
    team_links: list["TeamUserLink"] = Relationship(back_populates="user")
