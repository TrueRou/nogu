# #!/usr/bin/env python3.9
from __future__ import annotations

import pprint
import sys

from fastapi import status, FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import ORJSONResponse
from fastapi.responses import Response
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware

from app import database
from app.api import router
from app.database import db_session
from app.logging import log, Ansi


def init_exception_handlers(asgi_app: FastAPI) -> None:
    @asgi_app.exception_handler(RequestValidationError)
    async def handle_validation_error(
            request: Request,
            exc: RequestValidationError,
    ) -> Response:
        """Wrapper around 422 validation errors to print out info for devs."""
        log(f"Validation error on {request.url}", Ansi.LRED)
        pprint.pprint(exc.errors())

        return ORJSONResponse(
            content={"detail": jsonable_encoder(exc.errors())},
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )


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
    init_exception_handlers(asgi_app)
    init_events(asgi_app)
    init_routes(asgi_app)

    return asgi_app


nogu_app = init_api()
