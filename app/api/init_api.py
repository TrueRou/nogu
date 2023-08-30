from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from app import database
from app.api import router
from app.database import db_session
from app.logging import log, Ansi


def init_openapi(asgi_app: FastAPI) -> None:
    asgi_app.openapi_schema = get_openapi(
        title="nogu-nekko",
        version="",
        routes=asgi_app.routes,
    )
    for _, method_item in asgi_app.openapi_schema.get('paths').items():
        for _, param in method_item.items():
            responses = param.get('responses')
            # remove 422 response, also can remove other status code
            if '422' in responses:
                del responses['422']


def init_middlewares(asgi_app: FastAPI) -> None:
    origins = [
        "http://localhost:5173",
    ]

    asgi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def init_events(asgi_app: FastAPI) -> None:
    @asgi_app.on_event("startup")
    async def on_startup() -> None:
        try:
            async with db_session() as session:
                await session.execute(text('SELECT 1'))
                # TODO: Sql migration
                await database.create_db_and_tables()
            log("Startup process complete.", Ansi.LGREEN)
        except OperationalError:
            log("Failed to connect to the database.", Ansi.RED)


def init_routes(asgi_app: FastAPI) -> None:
    asgi_app.include_router(router)


def init_api() -> FastAPI:
    """Create & initialize our app."""
    asgi_app = FastAPI()

    init_middlewares(asgi_app)
    init_events(asgi_app)
    init_routes(asgi_app)

    init_openapi(asgi_app)

    return asgi_app


nogu_app = init_api()
