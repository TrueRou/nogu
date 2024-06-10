import contextlib
from fastapi import Request, Response
from sqlalchemy import func
from sqlmodel import SQLModel, create_engine, Session, select
from sqlmodel.sql.expression import _T0, _TCCA, SelectOfScalar
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from nogu import config

engine = create_engine(config.mysql_url)
async_engine = create_async_engine(config.mysql_url.replace("mysql+pymysql://", "mysql+aiomysql://"))


def create_db_and_tables(engine):
    import nogu.app.models  # make sure all models are imported (keep its record in metadata)

    nogu.app.models.SQLModel.metadata.create_all(engine)


def drop_db_and_tables(engine):
    import nogu.app.models  # make sure all models are imported (keep its record in metadata)

    nogu.app.models.SQLModel.metadata.drop_all(engine)


# https://stackoverflow.com/questions/75487025/how-to-avoid-creating-multiple-sessions-when-using-fastapi-dependencies-with-sec
def register_middleware(asgi_app):
    @asgi_app.middleware("http")
    async def session_middleware(request: Request, call_next):
        response = Response("Internal server error", status_code=500)
        try:
            with Session(engine, expire_on_commit=False) as session:
                request.state.session = session
                response = await call_next(request)
        finally:
            return response


def require_session(request: Request):
    return request.state.session


@contextlib.contextmanager
def session_ctx():
    with Session(engine, expire_on_commit=False) as session:
        yield session


@contextlib.asynccontextmanager
async def async_session_ctx():
    async with AsyncSession(async_engine) as session:
        yield session


def count(model: _TCCA[_T0]) -> SelectOfScalar[int]:
    return select(func.count()).select_from(model)


def add_model(session: Session, *models):
    [session.add(model) for model in models if model]
    session.commit()
    [session.refresh(model) for model in models if model]


def partial_update_model(session: Session, item: SQLModel, updates: SQLModel):
    if item and updates:
        update_data = updates.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(item, key, value)
        session.commit()
        session.refresh(item)
