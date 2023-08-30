from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sse_starlette import EventSourceResponse
from starlette.requests import Request

from app.api.schemas import APIResponse, docs
from app.api.schemas.beatmap import BeatmapBase, BeatmapEvent
from app.api.users import current_user
from app.database import db_session, async_session_maker
from app.definition import Operator
from app.interaction import Beatmap, User
from app.logging import log, Ansi


class BeatmapRequestOperator(Operator):
    db_session: AsyncSession = async_session_maker()

    async def operate(self, session: str, args: str) -> APIResponse:
        beatmap = await Beatmap.from_ident(self.db_session, session)
        if beatmap is not None:
            return APIResponse(info="Located", beatmap=BeatmapBase.from_orm(beatmap))
        beatmap = await Beatmap.request_api(args)
        if beatmap is not None:
            return APIResponse(info="Requested", beatmap=BeatmapBase.from_orm(beatmap))
        return APIResponse(success=False, info="Beatmap not found.")


router = APIRouter(prefix='/beatmaps', tags=['beatmaps'])
beatmap_request_operator = BeatmapRequestOperator()


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
