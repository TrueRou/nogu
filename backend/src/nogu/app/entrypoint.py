from __future__ import annotations

import asyncio
from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError, OperationalError
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from nogu.app import database, api
from nogu.app.database import session_ctx
from nogu.app.logging import log, Ansi
from nogu.app.api.users import parse_exception
from nogu.app.constants.exceptions import APIException
from nogu.app.api.osu import beatmaps, scores

keeping_tasks: list[asyncio.Task] = []


def init_openapi(asgi_app: FastAPI) -> None:
    asgi_app.openapi_schema = get_openapi(
        title="nogu-nekko",
        version="",
        routes=asgi_app.routes,
    )
    for _, method_item in asgi_app.openapi_schema.get("paths").items():
        for _, param in method_item.items():
            for key in list(param["responses"].keys()):
                # Remove 4xx and 5xx responses from the OpenAPI schema
                if key.startswith("4") or key.startswith("5"):
                    del param["responses"][key]


def init_middlewares(asgi_app: FastAPI) -> None:
    origins = [
        "http://localhost:5173",
        "http://localhost:3000",
    ]

    asgi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    database.register_middleware(asgi_app)


def init_events(asgi_app: FastAPI) -> None:
    @asgi_app.on_event("startup")
    async def on_startup() -> None:
        try:
            with session_ctx() as session:
                keeping_tasks.append(asyncio.create_task(beatmaps.beatmap_request_operator.operate_async()))
                keeping_tasks.append(asyncio.create_task(scores.bancho_match_inspector.inspect_async()))
                session.exec(text("SELECT 1"))
                database.create_db_and_tables(database.engine)  # TODO: Sql migration
                log("Startup process complete.", Ansi.LGREEN)
        except OperationalError:
            log("Failed to connect to the database.", Ansi.RED)

    @asgi_app.on_event("shutdown")
    async def on_shutdown() -> None:
        [task.cancel() for task in keeping_tasks]
        await database.async_engine.dispose()
        database.engine.dispose()


def init_exception_handlers(asgi_app: FastAPI) -> None:
    @asgi_app.exception_handler(IntegrityError)
    async def integrity_error_handler(request, exception: IntegrityError):
        log(f"Integrity error: {exception}", Ansi.RED)
        return APIException("Integrity error", "database", status.HTTP_409_CONFLICT).response()

    @asgi_app.exception_handler(APIException)
    async def api_exception_handler(request, exception: APIException):
        return exception.response()  # normalize response (with header)

    @asgi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, error: RequestValidationError):
        details_list = []
        for error in error.errors():
            details_list.append({"message": str(error), "i18n_node": ""})
        validation_err = APIException(f"Validation error", "validation", status.HTTP_422_UNPROCESSABLE_ENTITY)
        return validation_err.extends(details_list).response()

    @asgi_app.exception_handler(HTTPException)
    async def exception_handler(request, error: HTTPException):
        if error.headers == {"exception-source": "internal"}:
            return error
        return parse_exception(error).response({"exception-source": "fastapi-users"})


def init_routes(asgi_app: FastAPI) -> None:
    @asgi_app.get("/")
    async def root():
        return {"message": "Welcome to nogu-nekko!"}

    asgi_app.include_router(api.router)


def init_api() -> FastAPI:
    """Create & initialize our app."""
    asgi_app = FastAPI()

    init_middlewares(asgi_app)
    init_events(asgi_app)
    init_exception_handlers(asgi_app)
    init_routes(asgi_app)

    init_openapi(asgi_app)

    return asgi_app


nogu_app = init_api()
