import aiohttp
from orjson import orjson

http_client = aiohttp.ClientSession(json_serialize=lambda x: orjson.dumps(x).decode())