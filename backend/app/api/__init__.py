from fastapi import Depends, APIRouter

from app.api import users
from app.api.schemas import APIExceptions
from app.api.schemas.user import UserUpdate, UserBase, UserWrite, UserRead
from app.database import db_session
from app.services import User, Team, Stage, Score

router = APIRouter()

user_router = users.fastapi_users.get_users_router(UserRead, UserUpdate)
router.include_router(users.fastapi_users.get_auth_router(users.auth_backend), prefix="/auth/jwt", tags=["auth"])
router.include_router(users.fastapi_users.get_register_router(UserBase, UserWrite), prefix="/auth", tags=["auth"])

router.include_router(user_router, prefix="/users", tags=["users"])

require_user = users.fastapi_users.current_user(active=True)
require_user_optional = users.fastapi_users.current_user(active=True, optional=True)


async def require_team(team_id: int, user: User = Depends(require_user)):
    async with db_session() as session:
        team = await Team.from_id(session, team_id)
        if team is None:
            raise APIExceptions.team_not_exist
        if not await team.member_of(user):
            raise APIExceptions.team_not_belongings
        return team


async def require_stage(stage_id: int, user: User = Depends(require_user_optional)):
    # TODO... fix user privilege
    async with db_session() as session:
        stage = await Stage.from_id(session, stage_id)
        if stage is None:
            raise APIExceptions.stage_not_exist
        if not await stage.team.member_of(user):
            raise APIExceptions.team_not_belongings
        return stage


async def require_score(score_id: int, user: User = Depends(require_user)):
    async with db_session() as session:
        score = await Score.from_id(session, score_id)
        if score is None:
            raise APIExceptions.score_not_exist
        if score.user_id != user.id:
            raise APIExceptions.score_not_belongings
        return score
