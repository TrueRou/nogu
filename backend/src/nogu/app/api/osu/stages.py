from fastapi import APIRouter, Depends, Security
from fastapi.security import SecurityScopes
from nogu.app.models.osu.stage import StageMapUser, StageUser
from nogu.app.models.team import Team, TeamSrv
from nogu.app.models.user import User, UserSrv
from sqlalchemy import ScalarResult
from sqlmodel import Session, select

from nogu.app.models.osu import *
from nogu.app.database import require_session, add_model, partial_update_model

router = APIRouter(prefix="/stages", tags=["osu-stages"])


@router.get("/{stage_id}", response_model=Stage)
async def get_stage(stage: Stage = Security(StageSrv.require_stage)):
    return stage


@router.post("/", response_model=Stage)
async def create_stage(
    stage: StageBase,
    session: Session = Depends(require_session),
    team: Team = Security(TeamSrv.require_team, scopes=["admin"]),
    user: User = Depends(UserSrv.require_user),
):
    prepend_beatmaps: ScalarResult[PlaylistMap] = None
    if stage.playlist_id is not None:
        playlist: Playlist = PlaylistSrv.require_playlist(SecurityScopes(["access"]), stage.playlist_id, session, user)
        stage = StageBase(**playlist.model_dump(include={"ruleset", "win_condition"}))
        prepend_beatmaps = session.exec(select(PlaylistMap).where(PlaylistMap.playlist_id == playlist.id))
    stage = Stage(**stage.model_dump(), team_id=team.id)
    add_model(session, stage)
    if prepend_beatmaps is not None:
        for playlist_map in prepend_beatmaps:
            model = StageMap(**playlist_map.model_dump(exclude={"playlist_id", "condition"}), stage_id=stage.id)
            session.add(model)
        session.commit()
    return stage


@router.patch("/{stage_id}", response_model=Stage)
async def patch_stage(
    stage_update: StageUpdate, session: Session = Depends(require_session), stage: Stage = Security(StageSrv.require_stage, scopes=["admin"])
):
    partial_update_model(session, stage, stage_update)
    return stage


@router.get("/beatmaps/", response_model=list[StageMapPublic])
async def get_stage_beatmaps(limit=20, offset=0, session: Session = Depends(require_session), stage: Stage = Security(StageSrv.require_stage)):
    sentence = select(StageMap).where(StageMap.stage_id == stage.id).limit(limit).offset(offset)
    beatmaps = session.exec(sentence).all()
    return beatmaps


@router.post("/beatmaps/")
async def add_stage_beatmaps(
    stage_maps: list[StageMapBase], session: Session = Depends(require_session), stage: Stage = Security(StageSrv.require_stage, scopes=["admin"])
):
    for stage_map in stage_maps:
        model = StageMap(**stage_map.model_dump(), stage_id=stage.id)
        session.add(model)
    session.commit()


@router.get("/sheet/", response_model=dict)
async def get_sheet(session: Session = Depends(require_session), stage: Stage = Security(StageSrv.require_stage, scopes=["access-sensitive"])):
    stage_maps = session.exec(select(StageMap, Beatmap).join(Beatmap).where(StageMap.stage_id == stage.id)).all()
    stage_users = session.exec(select(StageUser, User).join(User).where(StageUser.stage_id == stage.id)).all()
    stage_map_users = session.exec(select(StageMapUser).where(StageMapUser.stage_id == stage.id))
    rows, cols, cells = {}, {}, {}
    rows = {stage_user.user_id: {"username": user.username, "analysis": stage_user.analysis} for stage_user, user in stage_users}
    cols = {stage_map.map_md5: StageMapSrv.as_col(stage_map, beatmap) for stage_map, beatmap in stage_maps}
    for stage_map, _ in stage_maps:
        cells[stage_map.map_md5] = {}
        for stage_user, _ in stage_users:
            cells[stage_map.map_md5][stage_user.user_id] = None
    for stage_map_user in stage_map_users:
        cells[stage_map_user.map_md5][stage_map_user.user_id] = stage_map_user.analysis
    return {"rows": rows, "cols": cols, "cells": cells}
