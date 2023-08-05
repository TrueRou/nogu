import asyncio
import queue

from app.api.schemas.beatmaps import BeatmapRead
from app.interaction import Beatmap

beatmap_tasks: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
beatmap_results: dict[str, asyncio.Queue[BeatmapRead]] = {}

inspecting_matches: list[int] = []


def is_empty_queue(dict_queue: dict, ident: str):
    return dict_queue[ident] is not None and not dict_queue[ident].empty()


def schedule_tasks():
    asyncio.create_task(consume_beatmap_tasks())


async def consume_beatmap_tasks():
    while True:
        (client_id, ident) = await beatmap_tasks.get()
        if ident is not None:
            if client_id not in beatmap_results:
                beatmap_results[client_id] = queue.Queue()
            await beatmap_results[client_id].put(BeatmapRead.from_orm(await Beatmap.request_api(ident)))


async def fetch_matches():
    pass
