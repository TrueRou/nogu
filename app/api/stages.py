from fastapi import APIRouter

from app import database
from app.api.schemas import docs, APIResponse
from app.api.schemas.beatmap import BeatmapBase
from app.api.schemas.stage import StageRead, StageBase, StageUpdate
from app.database import db_session
from app.interaction import Stage

router = APIRouter(prefix='/stages', tags=['stages'])


@router.get('/{stage_id}', responses=docs(StageRead))
async def get_stage(stage_id: int):
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            return APIResponse(success=False, info="Stage not found.")
        return APIResponse(stage=stage)


@router.put("/", responses=docs(StageBase))
async def create_stage(info: StageBase):
    async with db_session() as session:
        return APIResponse(stage=await database.add_model(session, Stage(**info.dict())))


@router.patch("/{stage_id}", responses=docs(StageRead))
async def patch_stage(stage_id: int, info: StageUpdate):
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            return APIResponse(success=False, info="Stage not found.")
        patched_stage = await database.partial_update(session, stage, info)
        return patched_stage


@router.get("/beatmaps/", responses=docs(list[BeatmapBase]))
async def get_beatmaps(stage_id: int, limit=20, offset=0):
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            return APIResponse(success=False, info="Stages not found.")
        beatmaps = await stage.get_beatmaps(limit, offset)
        return APIResponse(beatmaps=beatmaps)


@router.post("/beatmaps/", responses=docs(list[BeatmapBase]))
async def add_beatmaps(stage_id: int, beatmap_hashes: list[str]):
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            return APIResponse(success=False, info="Stages not found.")
        for md5 in beatmap_hashes:
            pass

