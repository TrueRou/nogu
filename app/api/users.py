import asyncio
from typing import Optional

import aiohttp
from fastapi import APIRouter, Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin, schemas, models, exceptions
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from starlette.requests import Request
from starlette.responses import RedirectResponse

import config
from app import database, sessions
from app.constants.servers import Server
from app.database import db_session
from app.interaction import User, UserAccount
from config import jwt_secret

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
current_user_optional = fastapi_users.current_user(active=True, optional=True)

router_extends = APIRouter()


async def get_oauth_server_user(code: str):
    http_client = await sessions.new_http_client()
    server_user = None
    result = await (await http_client.post("https://osu.ppy.sh/oauth/token", data={
        "client_id": config.osu_api_v2_id,
        "client_secret": config.osu_api_v2_secret,
        "redirect_uri": config.osu_api_v2_callback,
        "code": code,
        "grant_type": "authorization_code"
    })).json()
    if result["access_token"] is not None:
        server_user = await (await http_client.get("https://osu.ppy.sh/api/v2/me", headers={
            "Authorization": "Bearer " + result["access_token"]
        })).json()
    await http_client.close()
    return server_user


# https://osu.ppy.sh/oauth/authorize?client_id=14308&redirect_uri=http://localhost:8000/users/oauth/bancho/token&response_type=code&scope=identify
@router_extends.get("/oauth/bancho/token")
async def oauth_token(code: str, user: User = Depends(current_user_optional)):
    response = "/redirect?status=success&target=home"
    async with db_session() as session:
        if user is None:
            response = "/redirect?status=failure&target=login&reason=not_logged"
        user_account = await UserAccount.from_user_server(session, Server.BANCHO, user)
        new_server_user = await get_oauth_server_user(code)

        if new_server_user is None:
            response = "/redirect?status=failure&target=oauth&reason=oauth_failure"
            return RedirectResponse(sessions.get_uri() + response)

        # We have user account, check whether it is the original player
        if user_account is not None:
            if user_account.server_user_id == new_server_user['id']:
                user_account.server_user_name = new_server_user['username']
                asyncio.ensure_future(UserAccount.prepare_avatar(user=user, avatar_url=new_server_user['avatar_url']))
            else:
                response = "/redirect?status=failure&target=login&reason=not_the_same_account"
        else:
            # Register for the first time, check whether its occupied

            if await UserAccount.from_server_user_id(session, Server.BANCHO, new_server_user['id']) is not None:
                response = "/redirect?status=failure&target=oauth&reason=user_occupied"
            asyncio.ensure_future(UserAccount.prepare_avatar(user=user, avatar_url=new_server_user['avatar_url']))
            user_account = UserAccount(user_id=user.id, server_id=Server.BANCHO.value,
                                       server_user_id=new_server_user['id'],
                                       server_user_name=new_server_user['username'])
            await database.add_model(session, user_account)
    return RedirectResponse(sessions.get_uri() + response)
