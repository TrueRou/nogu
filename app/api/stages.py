from fastapi import APIRouter, Depends

from app import database
from app.api.schemas import docs, APIResponse, APIException
from app.api.schemas.beatmap import BeatmapBase
from app.api.schemas.stage import StageRead, StageBase, StageUpdate, StageMapBase
from app.api.users import current_user
from app.database import db_session
from app.interaction import Stage, User

router = APIRouter(prefix='/stages', tags=['stages'])


async def require_stage(stage_id: int, session=Depends(db_session), user: User = Depends(current_user)):
    stage = await Stage.from_id(session, stage_id)
    if stage is None:
        raise APIException(info="Stage not found.")
    if not await stage.team.member_of(user):
        raise APIException(info="Not a member of the team.")
    return stage


@router.get('/{stage_id}', responses=docs(StageRead))
async def get_stage(stage: Stage = Depends(require_stage)):
    return APIResponse(stage=stage)


@router.put("/", responses=docs(StageBase))
async def create_stage(info: StageBase):
    async with db_session() as session:
        return APIResponse(stage=await database.add_model(session, Stage(**info.dict())))


@router.patch("/{stage_id}", responses=docs(StageRead))
async def patch_stage(info: StageUpdate, stage: Stage = Depends(require_stage), session=Depends(db_session)):
    patched_stage = await database.partial_update(session, stage, info)
    return patched_stage


@router.get("/beatmaps/", responses=docs(list[BeatmapBase]))
async def get_beatmaps(limit=20, offset=0, stage: Stage = Depends(require_stage)):
    beatmaps = await stage.get_beatmaps(limit, offset)
    return APIResponse(beatmaps=beatmaps)


@router.post("/beatmaps/", responses=docs(list[BeatmapBase]))
async def add_beatmaps(stage_maps: list[StageMapBase], stage: Stage = Depends(require_stage)):
    for stage_map in stage_maps:
        await stage.add_beatmap(stage_map.dict())
