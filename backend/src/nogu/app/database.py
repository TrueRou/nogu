import contextlib
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from nogu import config

engine = create_engine(config.mysql_url, echo=False, future=True)
async_engine = create_async_engine(config.mysql_url.replace("mysql+pymysql://", "mysql+aiomysql://"), echo=False, future=True)


def create_db_and_tables(engine):
    import nogu.app.models  # make sure all models are imported (keep its record in metadata)

    nogu.app.models.SQLModel.metadata.create_all(engine)


def drop_db_and_tables(engine):
    import nogu.app.models  # make sure all models are imported (keep its record in metadata)

    nogu.app.models.SQLModel.metadata.drop_all(engine)


@contextlib.contextmanager
def manual_session():
    with Session(engine) as session:
        yield session


@contextlib.contextmanager
def auto_session():
    with Session(engine) as session:
        yield session
        session.commit()


@contextlib.asynccontextmanager
async def async_session():
    async with AsyncSession(async_engine) as session:
        yield session


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
