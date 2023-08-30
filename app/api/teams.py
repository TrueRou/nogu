from fastapi import APIRouter

from app import database
from app.api.schemas import APIResponse, docs
from app.api.schemas.score import ScoreRead
from app.api.schemas.stage import StageRead
from app.api.schemas.team import TeamBase, TeamRead, TeamUpdate
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


@router.patch('/{team_id}', responses=docs(TeamRead))
async def patch_team(team_id: int, info: TeamUpdate):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            return APIResponse(success=False, info="Team not found.")
        patched_team = await database.partial_update(session, team, info)
        return APIResponse(team=patched_team)


@router.get("/scores/", responses=docs(list[ScoreRead]))
async def get_recent_scores(team_id: int, limit=20, offset=0):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            return APIResponse(success=False, info="Team not found.")
        if team.active_stage is None:
            return APIResponse(success=False, info="Team has no active stage.")
        return APIResponse(scores=team.active_stage.get_scores(limit, offset))


@router.get("/stages", responses=docs(list[StageRead]))
async def get_stages(team_id: int, limit=20, offset=0):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            return APIResponse(success=False, info="Team not found.")
        return APIResponse(stages=await team.get_stages(limit, offset))
