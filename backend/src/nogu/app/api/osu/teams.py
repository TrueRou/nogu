from typing import Optional
from fastapi import APIRouter, Depends, Security
from nogu.app.models.combination import OsuTeamCombination, from_tuple
from nogu.app.models.team import TeamVisibility
from nogu.app.models.user import UserSrv
from sqlalchemy import func
from sqlmodel import Session, select
from nogu.app.models.osu import *
from nogu.app.models import Team, User, TeamSrv, TeamBase, TeamRole, TeamUserLink
from nogu.app.database import require_session, add_model, partial_update_model

router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[OsuTeamCombination])
async def get_teams(limit: int = 20, offset: int = 0, status: int = -1, session: Session = Depends(require_session)):
    StageSq = select(Stage.team_id, func.max(Stage.id).label("max_id")).group_by(Stage.team_id).subquery()
    sentence = (
        select(Team, Stage)
        .join(StageSq, onclause=Team.id == StageSq.c.team_id, isouter=True)
        .join(Stage, onclause=Stage.id == StageSq.c.max_id, isouter=True)
        .where(Team.visibility == TeamVisibility.PUBLIC)
        .limit(limit)
        .offset(offset)
        .order_by(Team.updated_at.desc())
    )
    if status == 0:
        sentence = sentence.where(Team.active == True)
    if status == 1:
        sentence = sentence.where(Team.active == False)
    results = session.exec(sentence).all()
    return from_tuple(results, OsuTeamCombination)


@router.get("/{team_id}", response_model=Optional[Team])
async def get_team(team: Team = Security(TeamSrv.require_team)):
    return team


@router.post("/{team_id}", response_model=Optional[Team])
async def create_team(team: TeamBase, session: Session = Depends(require_session), user: User = Depends(UserSrv.require_user)):
    team = Team(**team.model_dump())
    add_model(session, team)
    team_user = TeamUserLink(team_id=team.id, user_id=user.id, role=TeamRole.OWNER)
    add_model(session, team_user)
    return team


@router.patch("/{team_id}", response_model=Optional[Team])
async def patch_team(
    team_update: TeamBase, session: Session = Depends(require_session), team: Team = Security(TeamSrv.require_team, scopes=["admin"])
):
    session.refresh(team)
    partial_update_model(session, team, team_update)
    return team


@router.get("/me/", response_model=list[OsuTeamCombination])
async def get_teams_me(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(require_session),
    user: User = Depends(UserSrv.require_user),
    status: int = -1,
):
    StageSq = select(Stage.team_id, func.max(Stage.id).label("max_id")).group_by(Stage.team_id).subquery()
    sentence = (
        select(Team)
        .join(TeamUserLink)
        .join(StageSq, onclause=Team.id == StageSq.c.team_id, isouter=True)
        .join(Stage, onclause=Stage.id == StageSq.c.max_id, isouter=True)
        .where(TeamUserLink.user_id == user.id)
        .limit(limit)
        .offset(offset)
        .order_by(Team.updated_at.desc())
    )
    if status == 0:
        sentence = sentence.where(Team.active == True)
    if status == 1:
        sentence = sentence.where(Team.active == False)
    results = session.exec(sentence).all()
    return from_tuple(results, OsuTeamCombination)


@router.get("/scores/", response_model=list[Score])
async def get_scores(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(require_session),
    team: Team = Security(TeamSrv.require_team, scopes=["access-sensitive"]),
):
    sentence = select(Score).join(Stage).where(Stage.team_id == team.id).limit(limit).offset(offset).order_by(Score.id.desc())
    scores = session.exec(sentence).all()
    return scores


@router.get("/stages/", response_model=list[Stage])
async def get_stages(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(require_session),
    team: Team = Security(TeamSrv.require_team, scopes=["access-sensitive"]),
):
    sentence = select(Stage).where(Stage.team_id == team.id).limit(limit).offset(offset).order_by(Stage.updated_at.desc())
    stages = session.exec(sentence).all()
    return stages
