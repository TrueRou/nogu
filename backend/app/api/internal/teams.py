from fastapi import APIRouter, Depends

from app import database
from app.api import require_team, require_user_optional
from app.api.schemas import APIExceptions
from app.api.schemas.score import ScoreRead
from app.api.schemas.stage import StageRead
from app.api.schemas.team import TeamBase, TeamRead, TeamUpdate
from app.database import db_session
from app.interaction import Team, User
from app.constants.privacy import Privacy

router = APIRouter(prefix='/teams', tags=['teams'])


@router.get('/{team_id}', response_model=TeamRead)
async def get_team(team: Team = Depends(require_team)):
    return team


@router.get('/', response_model=list[TeamRead])
async def get_teams(privacy_limit: int, active_only: bool, limit: int = 20, offset: int = 0, user: User = Depends(require_user_optional)):
    async with db_session() as session:
        if privacy_limit == Privacy.PUBLIC: # the lowest scope
            teams = (await Team.fetch_all(session, limit, offset, with_private=False, active_only=active_only)).all()
        if privacy_limit > Privacy.PUBLIC: # the user's own teams
            if user is None:
                raise APIExceptions.user_unauthorized
            scalars = await Team.fetch_me(session, user) # no limitation here.
            teams = []
            for scalar in scalars:
                if active_only and scalar.teams.achieved:
                    continue
                teams.append(scalar.teams)
        return teams
    

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
        raise APIExceptions.team_active_stage_not_exist
    return team.active_stage.get_scores(limit, offset)


@router.get("/stages/", response_model=list[StageRead])
async def get_stages(limit: int = 20, offset: int = 0, team: Team = Depends(require_team)):
    return await team.get_stages(limit, offset)
