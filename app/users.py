from fastapi import Depends, HTTPException
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy import and_
from starlette import status

import services
from app import models
from app.models import User
from config import jwt_secret
from services import db_session


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    pass


async def get_user_manager():
    async with db_session() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, User))


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)


def current_team(user: User = Depends(current_user)) -> models.Team:
    if user.active_team is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Player has no active team.',
        )
    return user.active_team


async def current_stage(user: User = Depends(current_user)) -> models.Stage:
    active_team = current_team(user)
    if active_team.active_stage is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Team has no active stage.',
        )
    return active_team.active_stage


async def get_stage(stage_id: int, user: User = Depends(current_user)):
    async with db_session() as session:
        stage = await services.get_model(session, stage_id, models.Stage)
        member = await services.select_model(session, models.TeamMember, and_(models.TeamMember.team_id == stage.team_id, models.TeamMember.user_id == user.id))
        if member is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='You are not a team member of the stage.',
            )
        return stage

