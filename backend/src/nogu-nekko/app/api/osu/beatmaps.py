from fastapi import APIRouter, Depends
from sse_starlette import EventSourceResponse
from starlette.requests import Request

import config
from app.models.osu import *
from app.models.user import User
from app.api.users import require_user
from app.database import auto_session
from app.constants.exceptions import glob_not_exist
from app.objects import Operator
from app.logging import log, Ansi


class BeatmapRequestOperator(Operator):
    async def operate(self, session: str, args: str) -> BeatmapEvent:
        with auto_session() as db_session:
            beatmap = BeatmapSrv.from_ident(db_session, args)
            if beatmap is not None:
                self.skip_next_interval = True
            if beatmap is None:
                beatmap = await BeatmapSrv.request_api(args)
            if beatmap is None:
                return BeatmapEvent(message="Beatmap not found.")
            return BeatmapEvent(beatmap=beatmap)


router = APIRouter(prefix="/beatmaps", tags=["beatmaps"])
beatmap_request_operator = BeatmapRequestOperator(interval=config.beatmap_requests_interval)


@router.get("/{ident}", response_model=Beatmap)
async def get_beatmap(ident: str):
    async with auto_session() as session:
        beatmap = BeatmapSrv.from_ident(session, ident)
        if beatmap is None:
            raise glob_not_exist
        return beatmap


@router.post("/stream/")
async def stream_beatmap(request: Request, idents: list[str], user: User = Depends(require_user)):
    log(
        f"Doing beatmap streaming: {user.username} ({str(len(idents))} maps)",
        Ansi.LYELLOW,
    )
    for ident in idents:
        await beatmap_request_operator.new_operation(str(user.id), ident)
    return EventSourceResponse(beatmap_request_operator.event_generator(request, str(user.id)))
