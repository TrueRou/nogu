import aiohttp
from orjson import orjson
from ossapi import OssapiAsync

import config


async def new_http_client():
    return aiohttp.ClientSession(json_serialize=lambda x: orjson.dumps(x).decode())


api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)


def get_uri():
    debug_address = f"http://{config.bind_address}:{str(config.bind_port)}"
    return debug_address if config.debug else config.prod_address
