import aiohttp
from orjson import orjson
from ossapi import OssapiAsync

import config

http_client = aiohttp.ClientSession(json_serialize=lambda x: orjson.dumps(x).decode())
api_client = OssapiAsync(config.osu_api_v2_id, config.osu_api_v2_secret)
