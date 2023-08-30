import asyncio
from typing import Optional

from fastapi import APIRouter, Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, schemas, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from oauthlib import oauth2
from starlette.requests import Request

import config
from app import database, sessions
from app.database import db_session
from app.interaction import User, UserAccount
from config import jwt_secret, osu_api_v2_id, osu_api_v2_callback, osu_api_v2_secret

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def create(
            self,
            user_create: schemas.UC,
            safe: bool = False,
            request: Optional[Request] = None,
    ) -> models.UP:
        async with db_session() as session:
            existing_user = await database.select_model(session, User, User.username == user_create.username)
            if existing_user is not None:
                raise exceptions.UserAlreadyExists()
        return await super().create(user_create, safe, request)


async def get_user_manager():
    async with db_session() as session:
        yield UserManager(SQLAlchemyUserDatabase(session, User))


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=jwt_secret, lifetime_seconds=60 * 60 * 24 * 30)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user = fastapi_users.current_user(active=True)

router_extends = APIRouter()


# https://osu.ppy.sh/oauth/authorize?client_id=14308&redirect_uri=http://localhost:8000/users/oauth/bancho/token&response_type=code&scope=identify
@router_extends.get("/oauth/bancho/token")
async def oauth_token(code: str, user: User = Depends(current_user)):
    if user is None:
        # TODO... redirect to failure page
        pass

    result = await (await sessions.http_client.post("https://osu.ppy.sh/oauth/token", {
        "client_id": config.osu_api_v2_id,
        "client_secret": config.osu_api_v2_secret,
        "redirect_uri": config.osu_api_v2_callback,
        "code": code,
        "grant_type": "authorization_code"
    })).json()
    server_user = await (await sessions.http_client.get("https://osu.ppy.sh/api/v2/me", headers={
        "Authorization": "Bearer " + result["access_token"]
    })).json()
    async with db_session() as session:
        asyncio.ensure_future(UserAccount.prepare_avatar(user=user, avatar_url=server_user['avatar_url']))
        account = UserAccount.from_bancho(server_user, user)
        await account.create_raw(session)


