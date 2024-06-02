from __future__ import annotations

import asyncio
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

from app import database, api
from app.database import manual_session
from app.logging import log, Ansi
from app.api.users import parse_exception
from app.constants.exceptions import APIException, glob_validation
from app.api.osu import beatmaps, scores


def init_openapi(asgi_app: FastAPI) -> None:
    asgi_app.openapi_schema = get_openapi(
        title="nogu-nekko",
        version="",
        routes=asgi_app.routes,
    )
    for _, method_item in asgi_app.openapi_schema.get("paths").items():
        for _, param in method_item.items():
            responses = param.get("responses")
            # remove 422 response, also can remove other status code
            if "422" in responses:
                del responses["422"]
            if "401" in responses:
                del responses["401"]


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


def init_events(asgi_app: FastAPI) -> None:
    @asgi_app.on_event("startup")
    async def on_startup() -> None:
        try:
            with manual_session() as session:
                asyncio.create_task(beatmaps.beatmap_request_operator.operate_async())
                asyncio.create_task(scores.bancho_match_inspector.inspect_async())
                session.exec(text("SELECT 1"))
                database.create_db_and_tables()  # TODO: Sql migration
                log("Startup process complete.", Ansi.LGREEN)
        except OperationalError:
            log("Failed to connect to the database.", Ansi.RED)


def init_exception_handlers(asgi_app: FastAPI) -> None:
    @asgi_app.exception_handler(APIException)
    async def api_exception_handler(request, exception: APIException):
        return exception.response()  # normalize response (with header)

    @asgi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, error: RequestValidationError):
        details_list = []
        for error in error.errors():
            details_list.append({"message": str(error), "i18n_node": ""})
        return glob_validation.extends(details_list).response()

    @asgi_app.exception_handler(HTTPException)
    async def exception_handler(request, error: HTTPException):
        if error.headers == {"exception-source": "internal"}:
            return error
        return parse_exception(error).response({"exception-source": "fastapi-users"})


def init_routes(asgi_app: FastAPI) -> None:
    @asgi_app.get("/")
    async def root():
        return {"message": "Welcome to nogu-nekko!"}

    response = {
        400: {
            "content": {
                "application/json": {
                    "example": {
                        "message": "Request body is invalid.",
                        "i18n_node": "glob.request.invalid",
                    }
                }
            }
        }
    }

    asgi_app.include_router(api.router, responses=response)


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
