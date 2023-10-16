from fastapi import Depends, APIRouter

from app.api import users
from app.api.schemas import APIException
from app.api.schemas.user import UserUpdate, UserBase, UserWrite, UserRead
from app.database import db_session
from app.interaction import User, Team, Stage, Score

router = APIRouter()

user_router = users.fastapi_users.get_users_router(UserRead, UserUpdate)
router.include_router(users.fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt")
router.include_router(users.fastapi_users.get_register_router(UserBase, UserWrite), prefix="/auth")

router.include_router(user_router, prefix="/users", tags=["users"])

require_user = users.fastapi_users.current_user(active=True)
require_user_optional = users.fastapi_users.current_user(active=True, optional=True)


async def require_team(team_id: int, user: User = Depends(require_user)):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            raise APIException(message="Stage not found.")
        if not await team.member_of(user):
            raise APIException(message="Not a member of the team.")
        return team


async def require_stage(stage_id: int, user: User = Depends(require_user_optional)):
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            raise APIException(message="Stage not found.")
        if not await stage.team.member_of(user):
            raise APIException(message="Not a member of the team.")
        return stage


async def require_score(score_id: int, user: User = Depends(require_user)):
    async with db_session() as session:
        score = await Score.from_id(session, score_id)
        if score is None:
            raise APIException(message="Score not found.")
        if score.user_id != user.id:
            raise APIException(message="No permission.")
        return score
