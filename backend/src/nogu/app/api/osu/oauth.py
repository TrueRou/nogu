import ossapi
from fastapi import Depends, APIRouter
from ossapi import Ossapi, OssapiAsync
from sqlmodel import select
from starlette.responses import RedirectResponse

from nogu import config
from nogu.app.api.users import require_user_optional
from nogu.app.constants.osu import Server
from nogu.app.database import auto_session
from nogu.app.models import User
from nogu.app.models.osu import *
from typing import Callable, Any

router = APIRouter(prefix="/oauth", tags=["oauth"])


def generate_redirect(path: str, message: str):
    return RedirectResponse(config.redirect_uri + f"/redirect?path={path}&message={message}")


async def safe_request(func: Callable[..., Any], *args, **kwargs) -> Any:
    try:
        return await func(*args, **kwargs)
    except Exception:
        return None


# Bancho OAuth2
# this link is only for debug and test
# TODO: fix the redirect_uri to the new "/bancho/token" endpoint
# https://osu.ppy.sh/oauth/authorize?client_id=14308&redirect_uri=http://localhost:8000/users/oauth/token&response_type=code&scope=identify


async def request_identity(code: str):
    try:
        user_context = Ossapi(
            config.osu_api_v2_id,
            config.osu_api_v2_secret,
            config.osu_api_v2_callback,
            access_token=code,
        )
        return user_context.get_me()
    except Exception:
        return None


@router.get("/bancho/token")
async def process_bancho_oauth(code: str, user: User = Depends(require_user_optional)):
    with auto_session() as session:
        if user is None:
            return generate_redirect("login", "You need to login first for this operation.")
        # get the previous user account from the database
        sentence = select(UserAccount).where(UserAccount.user_id == user.id, UserAccount.osu_server == Server.BANCHO)
        user_account: UserAccount = session.exec(sentence).first()
        # get the user information from the osu! API
        api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret, config.osu_api_v2_callback, access_token=code)
        api_user: ossapi.User = await safe_request(api_client.get_me)

        if api_user is None:
            return generate_redirect("home", "Failed to get user information from osu! API.")

        if user_account is not None:
            # we have user account, check whether it is the original player
            if user_account.su_id == api_user.id:
                # update to the newest status of the player
                user_account.su_name = api_user.username
                user_account.su_priv = 0  # TODO: add privilege (bot, admin, supporter, etc.)
                user_account.su_country = api_user.country_code
                user_account.su_playtime = api_user.statistics.play_time
            else:
                # the account is not the same as the original one
                return generate_redirect("home", "This not the original bancho player of this account.")
        else:
            # register for the first time, check whether its occupied
            sentence = select(UserAccount).where(UserAccount.su_id == api_user.id, UserAccount.osu_server == Server.BANCHO)
            original_account = session.exec(sentence).first()
            if original_account is not None:
                # the bancho account is occupied by another user
                return generate_redirect("home", "This bancho account has been occupied by another user.")
            # register the new bancho account for the user
            user_account = UserAccount(
                user_id=user.id,
                osu_server=Server.BANCHO,
                su_id=api_user.id,
                su_name=api_user.username,
                su_priv=0,  # TODO: add privilege (bot, admin, supporter, etc.)
                su_country=api_user.country_code,
                su_playtime=api_user.statistics.play_time,
            )
            session.add(user_account)
        return generate_redirect("home", "Successfully linked your bancho account.")
