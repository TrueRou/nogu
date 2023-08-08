from fastapi import APIRouter

from app import database
from app.api.schemas import APIResponse, docs
from app.api.schemas.team import TeamBase, TeamRead
from app.database import db_session
from app.interaction import Team

router = APIRouter(prefix='/teams', tags=['teams'])


@router.get('/{team_id}', responses=docs(TeamRead))
async def get_team(team_id: int):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            return APIResponse(success=False, info="Team not found.")
        return APIResponse(team=await Team.from_id(session, team_id))


@router.get('/{team_id}', responses=docs(TeamRead))
async def create_team(info: TeamBase):
    async with db_session() as session:
        return APIResponse(team=await database.add_model(session, Team(**info.dict())))
