import datetime
from enum import IntFlag, auto
from sqlalchemy import Column, DateTime, func
from sqlmodel import Field, SQLModel

from app.constants.osu import Server


class ServerPriv(IntFlag):
    UNRESTRICTED = auto()
    SUPPORTER = auto()
    ADMIN = auto()


class UserAccount(SQLModel, table=True):
    __tablename__ = "osu_accounts"

    user_id: int = Field(foreign_key="users.id", primary_key=True)
    osu_server: int = Field(default=Server.BANCHO, primary_key=True)
    su_id: int = Field(index=True)
    su_name: str = Field(index=True)
    su_priv: ServerPriv = Field(default=ServerPriv.UNRESTRICTED)
    su_country: str = Field(default="XX")
    su_playtime: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
