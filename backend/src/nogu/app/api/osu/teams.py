from typing import Optional
from fastapi import APIRouter, Depends, Security
from nogu.app.models.combination import OsuTeamCombination, from_tuple, from_tuples
from nogu.app.models.team import TeamVisibility
from nogu.app.models.user import UserSrv
from sqlalchemy import func
from sqlmodel import Session, select
from nogu.app.models.osu import *
from nogu.app.models import Team, User, TeamSrv, TeamUserLink
from nogu.app.database import require_session

router = APIRouter(prefix="/teams", tags=["osu-teams"])

StageSq = select(Stage.team_id, func.max(Stage.id).label("max_id")).group_by(Stage.team_id).subquery()


@router.get("/", response_model=list[OsuTeamCombination])
async def get_teams(limit: int = 20, offset: int = 0, status: int = -1, session: Session = Depends(require_session)):
    sentence = (
        select(Team, Stage)
        .join(StageSq, onclause=Team.id == StageSq.c.team_id, isouter=True)
        .join(Stage, onclause=Stage.id == StageSq.c.max_id, isouter=True)
        .where(Team.visibility >= TeamVisibility.PROTECTED)
        .limit(limit)
        .offset(offset)
        .order_by(Team.updated_at.desc())
    )
    if status == 0:
        sentence = sentence.where(Team.active == True)
    if status == 1:
        sentence = sentence.where(Team.active == False)
    results = session.exec(sentence).all()
    return from_tuples(results, OsuTeamCombination)


@router.get("/{team_id}", response_model=Optional[OsuTeamCombination])
async def get_team(team: Team = Security(TeamSrv.require_team), session: Session = Depends(require_session)):
    sentence = select(Stage).where(Stage.team_id == team.id).order_by(Stage.id.desc()).limit(1)
    stage = session.exec(sentence).first()
    return from_tuple((team, stage), OsuTeamCombination)


@router.get("/me/", response_model=list[OsuTeamCombination])
async def get_teams_me(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(require_session),
    user: User = Depends(UserSrv.require_user),
    status: int = -1,
):
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
    return from_tuples(results, OsuTeamCombination)


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
