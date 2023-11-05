from fastapi import APIRouter, Depends

from app import database
from app.api import require_team, require_user
from app.api.schemas import APIException
from app.api.schemas.score import ScoreRead
from app.api.schemas.stage import StageRead
from app.api.schemas.team import TeamBase, TeamRead, TeamUpdate
from app.database import db_session
from app.interaction import Team, User

router = APIRouter(prefix='/teams', tags=['teams'])


@router.get('/{team_id}', response_model=TeamRead)
async def get_team(team: Team = Depends(require_team)):
    return team

@router.get('/me/', response_model=list[TeamRead])
async def get_teams_me(limit: int = 20, offset: int = 0, active_only: bool = False, user: User = Depends(require_user)):
    async with db_session() as session:
        scalars = await Team.fetch_me(session, user, limit, offset, active_only)
        temp = scalars.all()
        teams = [relationship.teams for relationship in scalars.all()]
        return teams


@router.get('/all/', response_model=list[TeamRead])
async def get_teams_all(limit: int = 20, offset: int = 0, active_only: bool = False):
    async with db_session() as session:
        scalars = await Team.fetch_all(session, limit, offset, with_private=False, active_only=active_only)
        return scalars.all()


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
async def get_recent_scores(limit: int = 20, offset: int = 0, team: Team = Depends(require_team)):
    if team.active_stage is None:
        raise APIException(message="Team has no active stage.")
    return team.active_stage.get_scores(limit, offset)


@router.get("/stages/", response_model=list[StageRead])
async def get_stages(limit: int = 20, offset: int = 0, team: Team = Depends(require_team)):
    return await team.get_stages(limit, offset)
