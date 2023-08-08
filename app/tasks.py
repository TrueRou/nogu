import asyncio

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.api.schemas.beatmap import BeatmapBase, BeatmapEvent
from app.interaction import Beatmap

beatmap_tasks: asyncio.Queue[tuple[str, str]] = asyncio.Queue()
beatmap_events: dict[str, asyncio.Queue[BeatmapEvent]] = {}  # replace with redis expired

inspecting_matches: list[int] = []


async def event_generator(session_events: dict[str, asyncio.Queue], request: Request, session: str):
    while True:
        if await request.is_disconnected():
            break
        content: BaseModel = await session_events[session].get()
        yield content.json()


def prepare_beatmap_tasks(session: str):
    if session not in beatmap_events:
        beatmap_events[session] = asyncio.Queue()


async def produce_beatmap_tasks(db_session: AsyncSession, session: str, ident: str):
    prepare_beatmap_tasks(session)
    beatmap = await Beatmap.from_ident(db_session, ident)

    if beatmap is not None:
        event = BeatmapEvent(success="true", info="offline", beatmap=BeatmapBase.from_orm(beatmap))
        await beatmap_events[session].put(event)
    else:
        await beatmap_tasks.put((session, ident))


async def consume_beatmap_tasks():
    while True:
        (session, ident) = await beatmap_tasks.get()
        if ident is not None:
            beatmap = await Beatmap.request_api(ident)
            if beatmap is not None:
                event = BeatmapEvent(success="true", info="online", beatmap=BeatmapBase.from_orm(beatmap))
            else:
                event = BeatmapEvent(success="false", info="Beatmap identifier was not found online.")
            await beatmap_events[session].put(event)
