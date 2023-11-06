from __future__ import annotations

import asyncio

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from starlette.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException

import app.api.internal
from app import database
from app.api.internal import scores, beatmaps
from app.database import db_session
from app.logging import log, Ansi
from app.api.schemas import APIException
from app.api.users import parse_exception


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
                asyncio.create_task(beatmaps.beatmap_request_operator.operate_async())
                asyncio.create_task(scores.bancho_match_inspector.inspect_async())
            log("Startup process complete.", Ansi.LGREEN)
        except OperationalError:
            log("Failed to connect to the database.", Ansi.RED)
            
def init_exception_handlers(asgi_app: FastAPI) -> None:
    @asgi_app.exception_handler(APIException)
    async def api_exception_handler(request, exception: APIException):
        return exception.response()
    
    @asgi_app.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, error: RequestValidationError):
        error_detail = []
        for each_error in error.errors():
            error_detail.append({
                'message': each_error['msg'],
                'i18n_node': each_error['type']
            })
        return APIException('Validation error', 'validation', details=error_detail).response()
    
    @asgi_app.exception_handler(HTTPException)
    async def exception_handler(request, error: HTTPException):
        if (error.headers == {'exception-source': 'internal'}):
            return error
        return parse_exception(error).response({'exception-source': 'fastapi-users'})


def init_routes(asgi_app: FastAPI) -> None:
    asgi_app.include_router(app.api.internal.router)
    asgi_app.include_router(app.api.router)


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
