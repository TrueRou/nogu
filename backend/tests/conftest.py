import pytest
from sqlmodel import Session
from sqlalchemy import create_engine

from nogu import config
from nogu.app import database


@pytest.fixture(scope="session")
def database_engine():
    engine = create_engine(config.mysql_url + "-test", echo=False)  # use a different database for testing
    database.drop_db_and_tables(engine)  # drop the database before testing
    database.create_db_and_tables(engine)  # create the database before testing
    yield engine  # provide the fixture value


@pytest.fixture()
def db_session(database_engine):
    yield Session(database_engine)
