import datetime
from fastapi import APIRouter, Depends, status
from nogu.app import database
from nogu.app.constants.exceptions import APIException
from nogu.app.database import require_session
from nogu.app.models.team import TeamInvite, TeamUserLink
from nogu.app.models.user import User, UserSrv
from sqlmodel import Session, select

from .users import router as users_router
from .teams import router as teams_router
from .oauth import router as oauth_router
from .osu import router as osu_router

router = APIRouter()

router.include_router(users_router)
router.include_router(teams_router)
router.include_router(oauth_router)
router.include_router(osu_router)


@router.get("/invites/{invite_code}", response_model=TeamUserLink, tags=["teams"])
async def verify_invite(invite_code: str, session: Session = Depends(require_session), user: User = Depends(UserSrv.require_user)):
    invite = session.exec(select(TeamInvite).where(TeamInvite.invite_code == invite_code)).first()
    if invite is None:
        raise APIException("The invite code is invalid.", "team.invite-invalid", status.HTTP_404_NOT_FOUND)
    existence = session.exec(select(TeamUserLink).where(TeamUserLink.team_id == invite.team_id, TeamUserLink.user_id == user.id)).first()
    if existence is not None:
        raise APIException("You are already in that team.", "team.already-in", status.HTTP_400_BAD_REQUEST)
    if invite.expired_at < datetime.datetime.utcnow():
        raise APIException("The invite code is expired.", "team.invite-expired", status.HTTP_400_BAD_REQUEST)
    team_member = TeamUserLink(team_id=invite.team_id, user_id=user.id)
    database.add_model(session, team_member)
    return team_member
