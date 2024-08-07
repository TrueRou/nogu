import random
from typing import Optional
from fastapi import APIRouter, Depends, Security
from nogu.app.models.team import TeamBase, TeamInvite, TeamRole, TeamVisibility
from nogu.app.models.user import UserSrv
from sqlmodel import Session, select
from nogu.app.models.osu import *
from nogu.app.models import Team, User, TeamSrv, TeamUserLink
from nogu.app.database import add_model, partial_update_model, require_session


router = APIRouter(prefix="/teams", tags=["teams"])


@router.get("/", response_model=list[Team])
async def get_teams(limit: int = 20, offset: int = 0, status: int = -1, session: Session = Depends(require_session)):
    sentence = select(Team).where(Team.visibility >= TeamVisibility.PROTECTED).limit(limit).offset(offset).order_by(Team.updated_at.desc())
    if status == 0:
        sentence = sentence.where(Team.active == True)
    if status == 1:
        sentence = sentence.where(Team.active == False)
    teams = session.exec(sentence).all()
    return teams


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


@router.get("/me/", response_model=list[Team])
async def get_teams_me(
    limit: int = 20,
    offset: int = 0,
    session: Session = Depends(require_session),
    user: User = Depends(UserSrv.require_user),
    status: int = -1,
):
    sentence = select(Team).join(TeamUserLink).where(TeamUserLink.user_id == user.id).limit(limit).offset(offset).order_by(Team.updated_at.desc())
    if status == 0:
        sentence = sentence.where(Team.active == True)
    if status == 1:
        sentence = sentence.where(Team.active == False)
    teams = session.exec(sentence).all()
    return teams


@router.post("/{team_id}/invite", response_model=TeamInvite)
async def generate_invite(
    session: Session = Depends(require_session),
    team: Team = Security(TeamSrv.require_team, scopes=["admin"]),
):
    invite = session.exec(select(TeamInvite).where(TeamInvite.team_id == team.id)).first()
    if invite is None:
        invite_code = "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 8))
        while session.exec(select(TeamInvite).where(TeamInvite.invite_code == invite_code)).first() is not None:
            invite_code = "".join(random.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", 8))
        invite = TeamInvite(team_id=team.id, invite_code=invite_code)
        add_model(session, invite)
    else:
        invite.expired_at = TeamInvite.postpone()
        session.commit()
    return invite
