import ast
import asyncio
import inspect
import re
from abc import abstractmethod, ABCMeta
from typing import TypeVar, Generic, Any

from starlette.requests import Request

from app.api.schemas import ModelResponse
from app.logging import log

T = TypeVar('T')

IGNORED_BEATMAP_CHARS = dict.fromkeys(map(ord, r':\/*<>?"|'), None)
MD5_PATTERN = re.compile(r'^[a-fA-F0-9]{32}$')


# define the object without orm session
# this kind of object can only invoke methods end with "raw"
class Raw(Generic[T]):
    def __init__(self, obj: T):
        self.object: T = obj

    def __getattribute__(self, name):
        attribute = super().__getattribute__(name)
        if inspect.ismethod(attribute):
            if not name.endwith('_raw'):
                log(f'ORM object {type(self.object)} invoke a sql-related function ({name}) without database session. method invoke has been canceled')
                return  # cancel the method invoked
        return attribute

    def __getattr__(self, name):
        return getattr(self.object, name)


class AstChecker:
    def __init__(self, condition: str):
        self.condition = condition

    def check(self, variables):
        try:
            namespace = {}
            namespace.update(variables)
            tree = ast.parse(self.condition, mode='eval')
            return eval(compile(tree, filename='<ast>', mode='eval'), namespace)
        except SyntaxError:
            return False


class Inspector(metaclass=ABCMeta):
    inspecting_targets: list[Any] = []
    polling_cursor: dict[Any, int] = {}
    events: dict[Any, asyncio.Queue[Any]] = {}
    disable_cursor: bool = False
    use_events = False
    stop_when_disconnected = True
    interval: float = 10.0
    each_interval: float = 0.1

    def __init__(self, interval: float, each_interval: float):
        self.interval = interval
        self.each_interval = each_interval

    def new_target(self, target: Any):
        if target not in self.inspecting_targets:
            self.inspecting_targets.append(target)
        if target not in self.polling_cursor:
            self.polling_cursor[target] = 0
        if self.use_events and target not in self.events:
            self.events[target] = asyncio.Queue()

    def remove_target(self, target: Any):
        self.inspecting_targets.remove(target)
        if self.use_events:
            del (self.events[target])

    async def event_generator(self, request: Request, target: Any):
        while True:
            if await request.is_disconnected():
                if self.use_events and self.stop_when_disconnected:
                    self.remove_target(target)
                break
            content = await self.events[target].get()
            yield content

    @abstractmethod
    async def process_result(self, target: Any, obj: Any) -> Any:
        pass

    @abstractmethod
    async def consume(self, target: Any) -> int:
        pass

    async def resulting(self, target: Any, cursor: int, obj: Any):
        if cursor > self.polling_cursor[target] or self.disable_cursor:
            result = await self.process_result(target, obj)
            if self.use_events:
                await self.events[target].put(result)

    async def _consume(self, target: Any):
        cursor = await self.consume(target)
        self.polling_cursor[target] = cursor

    async def inspect_async(self):
        while True:
            for target in self.inspecting_targets:
                await self._consume(target)
                await asyncio.sleep(self.each_interval)
            await asyncio.sleep(self.interval)


class Operator(metaclass=ABCMeta):
    tasks: asyncio.Queue[tuple[Any, Any]] = asyncio.Queue()
    events: dict[Any, asyncio.Queue[ModelResponse]] = {}
    interval: float
    skip_next_interval: bool = False

    def __init__(self, interval=1.0):
        self.interval = interval

    async def event_generator(self, request: Request, session: Any):
        while True:
            if await request.is_disconnected():
                break
            content = await self.events[session].get()
            yield content.json()

    async def new_operation(self, session: Any, args: Any):
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
            if self.skip_next_interval:
                self.skip_next_interval = False
                continue
            await asyncio.sleep(self.interval)
