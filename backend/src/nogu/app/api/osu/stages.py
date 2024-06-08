from fastapi import APIRouter, Security
from nogu.app.models.team import Team, TeamSrv
from sqlmodel import select

from nogu.app.models.osu import *
from nogu.app.database import auto_session, manual_session, add_model, partial_update_model

router = APIRouter(prefix="/stages", tags=["stages"])


@router.get("/{stage_id}", response_model=Stage)
async def get_stage(stage: Stage = Security(StageSrv.get_stage)):
    return stage


@router.post("/", response_model=Stage)
async def create_stage(stage: StageBase, team: Team = Security(TeamSrv.get_team, scopes=["member"])):
    with manual_session() as session:
        stage = Stage(**stage.model_dump(), team_id=team.id)
        add_model(session, stage)
    return stage


@router.patch("/{stage_id}", response_model=Stage)
async def patch_stage(stage_update: StageUpdate, stage: Stage = Security(StageSrv.get_stage, scopes=["admin"])):
    with manual_session() as session:
        partial_update_model(session, stage, stage_update)
    return stage


@router.get("/beatmaps/", response_model=list[Beatmap])
async def get_stage_beatmaps(limit=20, offset=0, stage: Stage = Security(StageSrv.get_stage)):
    with auto_session() as session:
        sentence = select(StageMap).where(StageMap.stage_id == stage.id).limit(limit).offset(offset)
        beatmaps = session.exec(sentence).all()
    return beatmaps


@router.post("/beatmaps/")
async def add_stage_beatmaps(stage_maps: list[StageMapBase], stage: Stage = Security(StageSrv.get_stage, scopes=["admin"])):
    with auto_session() as session:
        for stage_map in stage_maps:
            model = StageMap(**stage_map.model_dump(), stage_id=stage.id)
            session.add(model)
