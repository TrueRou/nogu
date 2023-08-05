from typing import Optional

from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app import definition
from app.api.schemas.beatmaps import BeatmapRead
from app.constants import tasks
from app.constants.tasks import beatmap_tasks
from app.database import db_session
from app.interaction import Beatmap

router = APIRouter(prefix='/beatmaps')


async def _fetch_single_beatmap(session: AsyncSession, ident: str) -> Optional[Beatmap]:
    if ident.isnumeric():
        return await Beatmap.from_id(session, int(ident))
    if definition.MD5_PATTERN.match(ident):
        return await Beatmap.from_md5(session, ident)


@router.post('/{ident}', response_model=Optional[BeatmapRead])
async def get_beatmap(ident: str):
    async with db_session() as session:
        return await _fetch_single_beatmap(session, ident)


@router.post('/sse/{client_id}')
async def push_beatmaps(client_id: str, idents: list[str]):
    for ident in idents:
        await beatmap_tasks.put((client_id, ident))


@router.get('/sse/{client_id}')
async def open_stream(client_id: str, request: Request):
    async def event_generator():
        while True:
            if await request.is_disconnected():
                break
            if not tasks.is_empty_queue(tasks.beatmap_results, client_id):
                yield await tasks.beatmap_results[client_id].get()
    return EventSourceResponse(event_generator())

