from fastapi import APIRouter, Depends, Security
from nogu.app.models.user import User, UserSrv
from sqlmodel import Session, select

from nogu.app.models.osu import *
from nogu.app.database import require_session, add_model, partial_update_model

router = APIRouter(prefix="/playlists", tags=["osu-playlists"])


@router.get("/{playlist_id}", response_model=Playlist)
async def get_playlist(playlist: Playlist = Security(PlaylistSrv.require_playlist)):
    return playlist


@router.post("/", response_model=Playlist)
async def create_playlist(playlist: PlaylistBase, session: Session = Depends(require_session), user: User = Depends(UserSrv.require_user)):
    playlist = Playlist(**playlist.model_dump(), user_id=user.id)
    add_model(session, playlist)
    return playlist


@router.patch("/{playlist_id}", response_model=Playlist)
async def patch_playlist(
    playlist_update: PlaylistUpdate,
    session: Session = Depends(require_session),
    playlist: Playlist = Security(PlaylistSrv.require_playlist, scopes=["owner"]),
):
    partial_update_model(session, Playlist, playlist_update)
    return playlist


@router.get("/beatmaps/", response_model=list[PlaylistMapPublic])
async def get_playlist_beatmaps(
    limit=20, offset=0, session: Session = Depends(require_session), playlist: Playlist = Security(PlaylistSrv.require_playlist)
):
    sentence = select(PlaylistMap).where(PlaylistMap.playlist_id == playlist.id).limit(limit).offset(offset)
    beatmaps = session.exec(sentence).all()
    return beatmaps


@router.post("/beatmaps/")
async def add_playlist_beatmaps(
    playlist_maps: list[PlaylistMapBase],
    session: Session = Depends(require_session),
    playlist: Playlist = Security(PlaylistSrv.require_playlist, scopes=["owner"]),
):
    for playlist_map in playlist_maps:
        model = PlaylistMap(**playlist_map.model_dump(), playlist_id=playlist.id)
        session.add(model)
    session.commit()
