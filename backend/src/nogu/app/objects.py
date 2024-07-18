import ast
import asyncio
import re
from abc import abstractmethod, ABCMeta
from typing import TypeVar, Any
from pydantic import BaseModel, TypeAdapter
from sqlalchemy import JSON, TypeDecorator
from starlette.requests import Request

T = TypeVar("T")

IGNORED_BEATMAP_CHARS = dict.fromkeys(map(ord, r':\/*<>?"|'), None)
MD5_PATTERN = re.compile(r"^[a-fA-F0-9]{32}$")


class AstChecker:
    def __init__(self, condition: str):
        self.condition = condition

    def check(self, variables):
        try:
            namespace = {}
            namespace.update(variables)
            tree = ast.parse(self.condition, mode="eval")
            return eval(compile(tree, filename="<ast>", mode="eval"), namespace)
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
            del self.events[target]

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
    events: dict[Any, asyncio.Queue[Any]] = {}
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


class PydanticJson(TypeDecorator):
    impl = JSON
    cache_ok = True

    def __init__(self, model: type[BaseModel]):
        super().__init__(none_as_null=True)
        self.model = model

    def result_processor(self, dialect, coltype):
        string_process = self._str_impl.result_processor(dialect, coltype)
        json_deserializer = TypeAdapter(self.model).validate_json

        def process(value):
            if value is None or value == "{}":
                return None
            if string_process:
                value = string_process(value)
            return json_deserializer(value)

        return process
