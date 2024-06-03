from fastapi import APIRouter, Depends
from sqlmodel import select

from nogu.app.api.users import require_user
from nogu.app.constants.exceptions import glob_not_belongings
from nogu.app.models.osu import *
from nogu.app.models import Team, User, TeamSrv, TeamBase, TeamRole, TeamUserLink
from nogu.app.database import auto_session, manual_session, add_model, partial_update_model

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[Team])
async def get_teams(limit: int = 20, offset: int = 0, active_only: bool = False):
    with auto_session() as session:
        sentence = select(Team).limit(limit).offset(offset).order_by(Team.updated_at)
        if active_only:
            sentence = sentence.where(Team.active == True)
        teams = session.exec(sentence).all()
    return teams


@router.get("/{team_id}", response_model=Team)
async def get_team(team_id: int, user: User = Depends(require_user)):
    with auto_session() as session:
        team = session.get(Team, team_id)
        if not TeamSrv.check_belongings(session, team, user):
            raise glob_not_belongings

    return team


@router.post("/{team_id}", response_model=Team)
async def create_team(team: TeamBase, user: User = Depends(require_user)):
    with manual_session() as session:
        team = Team(**team.model_dump())
        team_user = TeamUserLink(team_id=team.id, user_id=user.id, role=TeamRole.OWNER)
        add_model(session, team, team_user)
    return team


@router.patch("/{team_id}", response_model=Team)
async def patch_team(team_id: int, team_update: TeamBase, user: User = Depends(require_user)):
    with manual_session() as session:
        team = session.get(Team, team_id)
        if not TeamSrv.check_belongings(session, team, user):
            raise glob_not_belongings
        partial_update_model(session, team, team_update)
    return team


@router.get("/me", response_model=list[Team])
async def get_teams_me(limit: int = 20, offset: int = 0, user: User = Depends(require_user), active_only: bool = False):
    with auto_session() as session:
        sentence = select(Team).join(TeamUserLink).where(TeamUserLink.user_id == user.id).limit(limit).offset(offset).order_by(Team.updated_at)
        if active_only:
            sentence = sentence.where(Team.active == True)
        teams = session.exec(sentence).all()
    return teams


@router.get("/scores/", response_model=list[Score])
async def get_scores(team_id: int, limit: int = 20, offset: int = 0, user: User = Depends(require_user)):
    with auto_session() as session:
        team = session.get(Team, team_id)
        if not TeamSrv.check_belongings(session, team, user):
            raise glob_not_belongings
        sentence = select(Score).join(Stage).where(Stage.team_id == team_id).limit(limit).offset(offset)
        scores = session.exec(sentence).all()
    return scores


@router.get("/stages/", response_model=list[Stage])
async def get_stages(team_id: int, limit: int = 20, offset: int = 0, user: User = Depends(require_user)):
    with auto_session() as session:
        team = session.get(Team, team_id)
        if not TeamSrv.check_belongings(session, team, user):
            raise glob_not_belongings
        sentence = select(Stage).where(Stage.team_id == team_id).limit(limit).offset(offset)
        stages = session.exec(sentence).all()
    return stages
