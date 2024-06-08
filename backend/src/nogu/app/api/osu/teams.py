from typing import Optional
from fastapi import APIRouter, Depends, Security
from nogu.app.models.team import TeamVisibility, TeamWithMembers
from sqlmodel import select

from nogu.app.api.users import require_user
from nogu.app.models.osu import *
from nogu.app.models import Team, User, TeamSrv, TeamBase, TeamRole, TeamUserLink
from nogu.app.database import auto_session, manual_session, add_model, partial_update_model

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[TeamWithMembers])
async def get_teams(limit: int = 20, offset: int = 0, active_only: bool = False):
    with manual_session() as session:
        sentence = select(Team).where(Team.visibility == TeamVisibility.PUBLIC).limit(limit).offset(offset).order_by(Team.updated_at.desc())
        if active_only:
            sentence = sentence.where(Team.active == True)
        teams = session.exec(sentence).all()
    return teams


@router.get("/{team_id}", response_model=Optional[Team])
async def get_team(team: Team = Security(TeamSrv.get_team)):
    return team


@router.post("/{team_id}", response_model=Optional[Team])
async def create_team(team: TeamBase, user: User = Depends(require_user)):
    with manual_session() as session:
        team = Team(**team.model_dump())
        add_model(session, team)
        team_user = TeamUserLink(team_id=team.id, user_id=user.id, role=TeamRole.OWNER)
        add_model(session, team_user)
    return team


@router.patch("/{team_id}", response_model=Optional[Team])
async def patch_team(team_update: TeamBase, team: Team = Security(TeamSrv.get_team, scopes=["admin"])):
    with manual_session() as session:
        partial_update_model(session, team, team_update)
    return team


@router.get("/me/", response_model=list[Team])
async def get_teams_me(limit: int = 20, offset: int = 0, user: User = Depends(require_user), active_only: bool = False):
    with auto_session() as session:
        sentence = select(Team).join(TeamUserLink).where(TeamUserLink.user_id == user.id).limit(limit).offset(offset).order_by(Team.updated_at.desc())
        if active_only:
            sentence = sentence.where(Team.active == True)
        teams = session.exec(sentence).all()
    return teams


@router.get("/scores/", response_model=list[Score])
async def get_scores(limit: int = 20, offset: int = 0, team: Team = Security(TeamSrv.get_team, scopes=["access-sensitive"])):
    with auto_session() as session:
        sentence = select(Score).join(Stage).where(Stage.team_id == team.id).limit(limit).offset(offset).order_by(Score.id.desc())
        scores = session.exec(sentence).all()
    return scores


@router.get("/stages/", response_model=list[Stage])
async def get_stages(limit: int = 20, offset: int = 0, team: Team = Security(TeamSrv.get_team, scopes=["access-sensitive"])):
    with auto_session() as session:
        sentence = select(Stage).where(Stage.team_id == team.id).limit(limit).offset(offset).order_by(Stage.updated_at.desc())
        stages = session.exec(sentence).all()
    return stages
