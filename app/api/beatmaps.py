from typing import Optional

from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app.api.schemas.beatmaps import BeatmapBase
from app.api.users import current_user
from app import tasks
from app.database import db_session
from app.interaction import Beatmap, User
from app.tasks import event_generator, beatmap_events

router = APIRouter(prefix='/beatmaps', tags=['beatmaps'])


@router.get('/{ident}', response_model=Optional[BeatmapBase])
async def get_beatmap(ident: str):
    async with db_session() as session:
        return await Beatmap.from_ident(session, ident)


@router.post('/stream/')
async def stream_beatmap(request: Request, idents: list[str], user: User = Depends(current_user)):
    async with db_session() as session:
        for ident in idents:
            await tasks.produce_beatmap_tasks(session, str(user.id), ident)
    return EventSourceResponse(event_generator(beatmap_events, request, str(user.id)))
