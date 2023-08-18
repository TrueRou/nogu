import asyncio
from abc import ABCMeta, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from app.api.schemas import APIResponse
from app.api.schemas.beatmap import BeatmapBase
from app.database import async_session_maker
from app.interaction import Beatmap


class Operator(metaclass=ABCMeta):
    tasks: asyncio.Queue[tuple[Any, Any]] = asyncio.Queue()
    events: dict[Any, asyncio.Queue[BaseModel]] = {}
    interval: float

    def __init__(self, interval=1.0):
        self.interval = interval

    async def event_generator(self, request: Request, session: Any):
        while True:
            if await request.is_disconnected():
                break
            content = await self.events[session].get()
            yield content

    def new_operation(self, session: Any, args: Any):
        if session not in self.events:
            self.events[session] = asyncio.Queue()
        await self.tasks.put((session, args))

    @abstractmethod
    async def operate(self, session: Any, args: Any) -> Any:
        pass

    async def _operate(self, session: Any, args: Any):
        result = await self.operate(session, args)
        await self.events[session].put(result)

    async def operate_async(self):
        while True:
            (session, args) = await self.tasks.get()
            await self._operate(session, args)
            await asyncio.sleep(self.interval)


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
