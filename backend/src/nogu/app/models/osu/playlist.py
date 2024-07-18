import datetime
from enum import IntEnum, auto
from fastapi import Depends, status
from fastapi.security import SecurityScopes
from nogu.app.constants.exceptions import APIException
from nogu.app.database import require_session
from nogu.app.models.user import User, UserSrv
from nogu.app.utils import ensure_throw
from sqlmodel import Field, Relationship, SQLModel, Session

from nogu.app.constants.osu import Ruleset, WinCondition, Mods
from ..ast_condition import AstCondition, AstConditionPublic


class PlaylistVisibility(IntEnum):
    PUBLIC = auto()
    PRIVATE = auto()


class PlaylistBase(SQLModel):
    name: str = Field(index=True)
    description: str | None
    ruleset: Ruleset
    visibility: PlaylistVisibility = Field(default=PlaylistVisibility.PUBLIC)
    win_condition: WinCondition


class PlaylistUpdate(SQLModel):
    name: str | None
    description: str | None
    win_condition: WinCondition | None
    visibility: PlaylistVisibility | None


class Playlist(PlaylistBase, table=True):
    __tablename__ = "osu_playlists"

    id: int | None = Field(default=None, primary_key=True)
    version: int = Field(default=0)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    updated_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)  # we have to mannually update this column

    user_id: int = Field(foreign_key="users.id")


class PlaylistHistoryBase(SQLModel):
    playlist_id: int = Field(foreign_key="osu_playlists.id", primary_key=True)
    version: int = Field(primary_key=True)
    description: str | None


class PlaylistHistoryUpdate(SQLModel):
    description: str | None


class PlaylistHistory(PlaylistHistoryBase, table=True):
    __tablename__ = "osu_playlist_history"

    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)


class PlaylistMapBase(SQLModel):
    playlist_id: int = Field(foreign_key="osu_playlists.id", primary_key=True)
    map_md5: str = Field(foreign_key="osu_beatmaps.md5", primary_key=True)
    label: str  # NM1
    description: str | None  # Consistency Jumps
    represent_mods: Mods  # HDDTRX

    condition_id: int = Field(foreign_key="ast_conditions.id")


class PlaylistMapUpdate(SQLModel):
    label: str | None
    description: str | None
    represent_mods: Mods | None
    condition_id: int | None


class PlaylistMap(PlaylistMapBase, table=True):
    __tablename__ = "osu_playlist_maps"

    condition: AstCondition = Relationship()


class PlaylistMapPublic(PlaylistMapBase):
    condition: AstConditionPublic


class PlaylistSrv:
    def _ensure_ownership(session: Session, playlist: Playlist, user: User | None) -> tuple[bool, APIException]:
        if user is None:
            return False, APIException("Login is required to access that model.", "model.login-required", status.HTTP_401_UNAUTHORIZED)
        if playlist.user_id != user.id:
            return False, APIException("You have no privilege to do that.", "model.no-priv", status.HTTP_403_FORBIDDEN)
        return True, None

    # scope: access, owner
    def require_playlist(
        security: SecurityScopes,
        playlist_id: int,
        session: Session = Depends(require_session),
        user: User | None = Depends(UserSrv.require_user_optional),
    ):
        playlist = session.get(Playlist, playlist_id)
        if playlist is None:
            raise APIException("Playlist not found", "playlist.not-found", status.HTTP_404_NOT_FOUND)

        if "access" in security.scopes or security.scopes == []:
            if playlist.visibility == PlaylistVisibility.PRIVATE:
                ensure_throw(PlaylistSrv._ensure_ownership, session, playlist, user)

        if "owner" in security.scopes:
            ensure_throw(PlaylistSrv._ensure_ownership, session, playlist, user)

        return playlist
