import asyncio
from typing import Optional

from fastapi import APIRouter, Depends

from app.api.schemas.beatmaps import BeatmapBase, QueuedBeatmaps
from app.api.users import current_user
from app.constants import tasks
from app.constants.tasks import dump
from app.database import db_session
from app.interaction import Beatmap, User

router = APIRouter(prefix='/beatmaps', tags=['beatmaps'])


@router.get('/{ident}', response_model=Optional[BeatmapBase])
async def get_beatmap(ident: str):
    async with db_session() as session:
        return await Beatmap.from_ident(session, ident)


@router.post('/queue/')
async def queue_beatmaps(idents: list[str], user: User = Depends(current_user)):
    async with db_session() as session:
        for ident in idents:
            await tasks.produce_beatmap_tasks(session, user.id, ident)
    return await dequeue_beatmaps(user)


@router.get('/queue/', response_model=QueuedBeatmaps)
async def dequeue_beatmaps(user: User = Depends(current_user)):
    tasks.prepare_beatmap_tasks(user.id)
    return QueuedBeatmaps(
            results=await dump(tasks.beatmap_results[user.id]),
            failures=await dump(tasks.beatmap_failures[user.id])
        )

