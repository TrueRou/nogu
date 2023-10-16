import asyncio

import aiohttp
from fastapi import Depends, APIRouter
from starlette.responses import RedirectResponse

import config
from app import sessions, database
from app.api import require_user_optional
from app.constants.servers import Server
from app.database import db_session
from app.interaction import User, UserAccount

router = APIRouter(prefix='/oauth', tags=['oauth'])


# this link is only for debug and test
# https://osu.ppy.sh/oauth/authorize?client_id=14308&redirect_uri=http://localhost:8000/users/oauth/token&response_type=code&scope=identify

async def request_identity(code: str):
    async with aiohttp.ClientSession() as session:
        result = await (await session.post("https://osu.ppy.sh/oauth/token", data={
            "client_id": config.osu_api_v2_id,
            "client_secret": config.osu_api_v2_secret,
            "redirect_uri": config.osu_api_v2_callback,
            "code": code,
            "grant_type": "authorization_code"
        })).json()
        if result["access_token"] is not None:
            return await (await session.get("https://osu.ppy.sh/api/v2/me", headers={
                "Authorization": "Bearer " + result["access_token"]
            })).json()


def generate_redirect(success: bool, **kwargs):
    status = "success" if success else "failure"
    path = f"/redirect?status={status}&"
    for key, item in kwargs:
        path += f"{key}={item}&"
    return RedirectResponse(sessions.get_uri() + path[:-1])


@router.get("/token")
async def process_oauth(code: str, user: User = Depends(require_user_optional)):
    async with db_session() as session:
        if user is None:
            return generate_redirect(success=False, target="login", reason="not_logged")
        user_account = await UserAccount.from_user_server(session, Server.BANCHO, user)
        api_user = await request_identity(code)

        if api_user is None:
            return generate_redirect(success=False, target="oauth", reason="identity_failure")

        if user_account is not None:
            # we have user account, check whether it is the original player
            if user_account.server_user_id == api_user['id']:
                # update for the newest username of the player
                user_account.server_user_name = api_user['username']
                await session.commit()
            else:
                return generate_redirect(success=False, target="oauth", reason="not_the_same_account")
        else:
            # register for the first time, check whether its occupied
            original_account = await UserAccount.from_source(session, Server.BANCHO, api_user['id'])
            if original_account is not None:
                return generate_redirect(success=False, target="oauth", reason="user_occupied")
            # do the insert operation
            user_account = UserAccount(user_id=user.id, server_id=Server.BANCHO.value,
                                       server_user_id=api_user['id'],
                                       server_user_name=api_user['username'])
            await database.add_model(session, user_account)
        asyncio.ensure_future(UserAccount.prepare_avatar(user=user, avatar_url=api_user['avatar_url']))
        return generate_redirect(success=True, target="home")
