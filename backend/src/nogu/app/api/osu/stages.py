from fastapi import APIRouter, Depends
from sqlmodel import select

from nogu.app.api.users import require_user
from nogu.app.models.osu import *
from nogu.app.models import User, TeamRole
from nogu.app.database import auto_session, manual_session, add_model, partial_update_model

router = APIRouter(prefix="/stages", tags=["stages"])


@router.get("/{stage_id}", response_model=Stage)
async def get_stage(stage_id: int, user: User = Depends(require_user)):
    with auto_session() as session:
        stage = session.get(Stage, stage_id)
        StageSrv.check_belongings(session, stage, user)
    return stage


@router.post("/", response_model=Stage)
async def create_stage(stage: StageBase, user: User = Depends(require_user)):
    with manual_session() as session:
        StageSrv.check_belongings(session, stage, user)
        stage = Stage(**stage.model_dump())
        add_model(session, stage)
    return stage


@router.patch("/{stage_id}", response_model=Stage)
async def patch_stage(stage_id: int, stage_update: StageUpdate, user: User = Depends(require_user)):
    with manual_session() as session:
        stage = session.get(Stage, stage_id)
        StageSrv.check_belongings(session, stage, user)
        partial_update_model(session, stage, stage_update)
    return stage


@router.get("/beatmaps/", response_model=list[Beatmap])
async def get_stage_beatmaps(stage_id: int, limit=20, offset=0, user: User = Depends(require_user)):
    with auto_session() as session:
        stage = session.get(Stage, stage_id)
        StageSrv.check_belongings(session, stage, user)
        sentence = select(StageMap).where(StageMap.stage_id == stage_id).limit(limit).offset(offset)
        beatmaps = session.exec(sentence).all()
    return beatmaps


@router.post("/beatmaps/")
async def add_stage_beatmaps(stage_id: int, stage_maps: list[StageMapBase], user: User = Depends(require_user)):
    with auto_session() as session:
        stage = session.get(Stage, stage_id)
        StageSrv.check_permission(session, stage, user, TeamRole.ADMIN)
        for stage_map in stage_maps:
            model = StageMap(**stage_map.model_dump())
            session.add(model)
