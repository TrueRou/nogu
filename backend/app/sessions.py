from ossapi import OssapiAsync

from app.logging import Ansi, log
import config

api_client: OssapiAsync = None

bancho_nogu_users: dict[int, int] = {}


async def init_sessions():
    global api_client
    try:
        api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)
    except Exception:
        log("Failed to connect to the osu!apiv2.", Ansi.RED)
        

def get_uri():
    debug_address = f"http://{config.bind_address}:{str(config.bind_port)}"
    return debug_address if config.debug else config.prod_address
