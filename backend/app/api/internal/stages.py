import asyncio

from fastapi import APIRouter, Depends

from app import database, analysis
from app.api import require_stage
from app.api.schemas.beatmap import BeatmapBase
from app.api.schemas.stage import StageRead, StageBase, StageUpdate, StageMapBase
from app.database import db_session
from backend.app.services import Stage

router = APIRouter(prefix='/stages', tags=['stages'])


@router.get('/{stage_id}', response_model=StageRead)
async def get_stage(stage: Stage = Depends(require_stage)):
    return stage


@router.post("/", response_model=StageBase)
async def create_stage(info: StageBase):
    async with db_session() as session:
        return await database.add_model(session, Stage(**info.dict()))


@router.patch("/{stage_id}", response_model=StageRead)
async def patch_stage(info: StageUpdate, stage: Stage = Depends(require_stage)):
    async with db_session() as session:
        patched_stage = await database.partial_update(session, stage, info)
        return patched_stage


@router.post('/{stage_id}')
async def begin_analysis_debug(stage_id: int):
    asyncio.ensure_future(analysis.process_async(stage_id))


@router.get("/beatmaps/", response_model=list[BeatmapBase])
async def get_beatmaps(limit=20, offset=0, stage: Stage = Depends(require_stage)):
    beatmaps = await stage.get_beatmaps(limit, offset)
    return beatmaps


@router.post("/beatmaps/", response_model=list[BeatmapBase])
async def add_beatmaps(stage_maps: list[StageMapBase], stage: Stage = Depends(require_stage)):
    for stage_map in stage_maps:
        await stage.add_beatmap(stage_map.dict())
