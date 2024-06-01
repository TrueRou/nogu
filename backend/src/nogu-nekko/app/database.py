import contextlib
from sqlmodel import SQLModel, create_engine, Session

import config

engine = create_engine(config.mysql_url, echo=False, future=True)


def create_db_and_tables():
    import app.models  # make sure all models are imported (keep its record in metadata)

    app.models.SQLModel.metadata.create_all(engine)


@contextlib.contextmanager
def manual_session():
    with Session(engine) as session:
        yield session


@contextlib.contextmanager
def auto_session():
    with Session(engine) as session:
        yield session
        session.commit()


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
