from fastapi import APIRouter, Depends

from app import database
from app.api.schemas import APIResponse, docs, APIException
from app.api.schemas.score import ScoreRead
from app.api.schemas.stage import StageRead
from app.api.schemas.team import TeamBase, TeamRead, TeamUpdate
from app.api.users import current_user
from app.database import db_session
from app.interaction import Team, User

router = APIRouter(prefix='/teams', tags=['teams'])


async def require_team(team_id: int, session=Depends(db_session), user: User = Depends(current_user)):
    stage = await Team.from_id(session, team_id)
    if stage is None:
        raise APIException(info="Stage not found.")
    return stage


@router.get('/{team_id}', responses=docs(TeamRead))
async def get_team(team: Team = Depends(require_team)):
    return APIResponse(team=team)


@router.get('/{team_id}', responses=docs(TeamRead))
async def create_team(info: TeamBase):
    async with db_session() as session:
        return APIResponse(team=await database.add_model(session, Team(**info.dict())))


@router.patch('/{team_id}', responses=docs(TeamRead))
async def patch_team(info: TeamUpdate, team: Team = Depends(require_team), session=Depends(db_session)):
    patched_team = await database.partial_update(session, team, info)
    return APIResponse(team=patched_team)


@router.get("/scores/", responses=docs(list[ScoreRead]))
async def get_recent_scores(limit=20, offset=0, team: Team = Depends(require_team)):
    if team.active_stage is None:
        raise APIException(info="Team has no active stage.")
    return APIResponse(scores=team.active_stage.get_scores(limit, offset))


@router.get("/stages", responses=docs(list[StageRead]))
async def get_stages(limit=20, offset=0, team: Team = Depends(require_team)):
    return APIResponse(stages=await team.get_stages(limit, offset))
