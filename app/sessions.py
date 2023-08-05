import aiohttp
from apscheduler.schedulers.background import BackgroundScheduler
from orjson import orjson

http_client = aiohttp.ClientSession(json_serialize=lambda x: orjson.dumps(x).decode())

scheduler = BackgroundScheduler()
