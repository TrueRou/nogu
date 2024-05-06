import asyncio

from fastapi import Depends, APIRouter
from ossapi import Ossapi
from starlette.responses import RedirectResponse

import config
from app import sessions, database
from app.api import require_user_optional
from app.constants.servers import Server
from app.database import db_session
from app.services import User, UserAccount

router = APIRouter(prefix='/oauth', tags=['oauth'])


# this link is only for debug and test
# https://osu.ppy.sh/oauth/authorize?client_id=14308&redirect_uri=http://localhost:8000/users/oauth/token&response_type=code&scope=identify

async def request_identity(code: str):
    try:
        user_context = Ossapi(config.osu_api_v2_id, config.osu_api_v2_secret, config.osu_api_v2_callback, access_token=code)
        return user_context.get_me()
    except Exception:
        return None


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
        user_account: UserAccount = await UserAccount.from_source(session, Server.BANCHO, user)
        api_user = await request_identity(code)

        if api_user is None:
            return generate_redirect(success=False, target="oauth", reason="identity_failure")

        if user_account is not None:
            # we have user account, check whether it is the original player
            if user_account.su_id == api_user.id:
                # update to the newest status of the player
                await user_account.refresh_user(api_user=api_user)
            else:
                return generate_redirect(success=False, target="oauth", reason="not_the_same_account")
        else:
            # register for the first time, check whether its occupied
            original_account = await UserAccount.from_source(session, Server.BANCHO, api_user['id'])
            if original_account is not None:
                return generate_redirect(success=False, target="oauth", reason="user_occupied")
            # do the insertion and refresh operation
            user_account = UserAccount(user_id=user.id, server_id=Server.BANCHO.value, server_user_id=api_user['id'])
            await database.add_model(session, user_account)
            await user_account.refresh_user(api_user=api_user) # fill other fields of the server user
        asyncio.ensure_future(UserAccount.prepare_avatar(user=user, avatar_url=api_user['avatar_url']))
        return generate_redirect(success=True, target="home")
