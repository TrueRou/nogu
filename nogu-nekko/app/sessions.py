from ossapi import OssapiAsync

import config

api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)

bancho_nogu_users: dict[int, int] = {}


def get_uri():
    debug_address = f"http://{config.bind_address}:{str(config.bind_port)}"
    return debug_address if config.debug else config.prod_address
