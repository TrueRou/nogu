import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas.beatmaps import BeatmapBase
from app.interaction import Beatmap

beatmap_tasks: asyncio.Queue[tuple[int, str]] = asyncio.Queue()
beatmap_results: dict[int, asyncio.Queue[BeatmapBase]] = {}
beatmap_failures: dict[int, asyncio.Queue[str]] = {}

inspecting_matches: list[int] = []


async def dump(queue: asyncio.Queue) -> list:
    result = []
    while not queue.empty():
        result.append(await queue.get())
    return result


def schedule_tasks():
    asyncio.create_task(consume_beatmap_tasks())


def prepare_beatmap_tasks(client_id: int):
    if client_id not in beatmap_results:
        beatmap_results[client_id] = asyncio.Queue()
    if client_id not in beatmap_failures:
        beatmap_failures[client_id] = asyncio.Queue()


async def produce_beatmap_tasks(session: AsyncSession, client_id: int, ident: str):
    prepare_beatmap_tasks(client_id)
    beatmap = await Beatmap.from_ident(session, ident)
    if beatmap is not None:
        await beatmap_results[client_id].put(BeatmapBase.from_orm(beatmap))
    else:
        await beatmap_tasks.put((client_id, ident))


async def consume_beatmap_tasks():
    while True:
        (client_id, ident) = await beatmap_tasks.get()
        if ident is not None:
            beatmap = await Beatmap.request_api(ident)
            if beatmap is not None:
                await beatmap_results[client_id].put(BeatmapBase.from_orm(beatmap))
            else:
                await beatmap_failures[client_id].put(ident)
