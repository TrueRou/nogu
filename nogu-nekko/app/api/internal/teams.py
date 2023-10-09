from fastapi import APIRouter, Depends

from app import database
from app.api import require_team
from app.api.schemas import APIException
from app.api.schemas.score import ScoreRead
from app.api.schemas.stage import StageRead
from app.api.schemas.team import TeamBase, TeamRead, TeamUpdate
from app.database import db_session
from app.interaction import Team

router = APIRouter(prefix='/teams', tags=['teams'])


@router.get('/{team_id}', response_model=TeamRead)
async def get_team(team: Team = Depends(require_team)):
    return team


@router.post('/{team_id}', response_model=TeamRead)
async def create_team(info: TeamBase):
    async with db_session() as session:
        return await database.add_model(session, Team(**info.dict()))


@router.patch('/{team_id}', response_model=TeamRead)
async def patch_team(info: TeamUpdate, team: Team = Depends(require_team)):
    async with db_session() as session:
        patched_team = await database.partial_update(session, team, info)
        return patched_team


@router.get("/scores/", response_model=list[ScoreRead])
async def get_recent_scores(limit=20, offset=0, team: Team = Depends(require_team)):
    if team.active_stage is None:
        raise APIException(message="Team has no active stage.")
    return team.active_stage.get_scores(limit, offset)


@router.get("/stages", response_model=list[StageRead])
async def get_stages(limit=20, offset=0, team: Team = Depends(require_team)):
    return await team.get_stages(limit, offset)
