from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app.api.schemas import APIResponse, docs
from app.api.schemas.beatmap import BeatmapBase, BeatmapEvent
from app.api.users import current_user
from app.database import db_session
from app.interaction import Beatmap, User
from app.logging import log, Ansi
from app.sessions import beatmap_request_operator

router = APIRouter(prefix='/beatmaps', tags=['beatmaps'])


@router.get('/{ident}', responses=docs(BeatmapBase))
async def get_beatmap(ident: str):
    async with db_session() as session:
        beatmap = await Beatmap.from_ident(session, ident)
        if beatmap is None:
            return APIResponse(success=False, info="Beatmap not found.")
        return APIResponse(beatmap=BeatmapBase.from_orm(beatmap))


@router.post('/stream/', responses=docs(BeatmapEvent))
async def stream_beatmap(request: Request, idents: list[str], user: User = Depends(current_user)):
    log(f"Doing beatmap streaming: {user.username} ({str(len(idents))} maps)", Ansi.LYELLOW)
    for ident in idents:
        await beatmap_request_operator.new_operation(str(user.id), ident)
    return EventSourceResponse(beatmap_request_operator.event_generator(request, str(user.id)))
