import asyncio
from abc import ABCMeta, abstractmethod
from typing import Any

from ossapi import MatchResponse, MatchEvent
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import scores
from app.constants.servers import Server
from app.database import async_session_maker
from app.interaction import User, Beatmap
from app.sessions import api_client


class Inspector(metaclass=ABCMeta):
    inspecting_targets: list[Any] = []
    polling_cursor: dict[Any, int] = {}
    disable_cursor: bool = False
    interval: float = 1.0

    def __init__(self, disable_cursor: bool, interval: float):
        self.disable_cursor = disable_cursor
        self.interval = interval

    def new_target(self, target: Any):
        if target not in self.inspecting_targets:
            self.inspecting_targets.append(target)
        if target not in self.polling_cursor:
            self.polling_cursor[target] = 0

    def remove_target(self, target: Any):
        self.inspecting_targets.remove(target)

    @abstractmethod
    async def process_result(self, target: Any, obj: Any):
        pass

    @abstractmethod
    async def consume(self, target: Any) -> int:
        pass

    async def resulting(self, target: Any, cursor: int, obj: Any):
        if cursor > self.polling_cursor[target] or self.disable_cursor:
            await self.process_result(target, obj)

    async def _consume(self, target: Any):
        cursor = await self.consume(target)
        self.polling_cursor[target] = cursor

    async def inspect_async(self):
        while True:
            for target in self.inspecting_targets:
                await self._consume(target)
                await asyncio.sleep(self.interval)


class BanchoMatchInspector(Inspector):
    db_session: AsyncSession = async_session_maker()

    async def consume(self, target: Any) -> int:
        match: MatchResponse = await api_client.match(target)
        if match.match.end_time is not None:
            self.remove_target(target)
        for event in match.events:
            await self.resulting(target, event.id, event)
        return match.latest_event_id

    async def process_result(self, target: Any, event: MatchEvent):
        for score in event.game.scores:
            user = await User.from_id(self.db_session, score.user_id, Server.BANCHO)
            if user is not None:
                beatmap = await Beatmap.from_id(self.db_session, event.game.beatmap_id)
                if beatmap is not None:
                    await scores.submit_score(scores.ScoreBase.from_ossapi(score, beatmap.md5, user.id), user)
        await self.db_session.commit()
