import pytest
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from sqlalchemy import MetaData, text
from sqlalchemy.orm import Session
from testcontainers.postgres import PostgresContainer

from src.app import create_app
from test.utils.app_test_context import AppTestContext

pytest_plugins = [
    'test.fixtures.services',
    'test.fixtures.repositories',
]


@pytest.fixture(scope='session')
def postgres():
    with PostgresContainer('postgres:16', driver='psycopg') as postgres:
        yield postgres


@pytest.fixture(scope='session')
def client_and_container(postgres):
    test_db_url = postgres.get_connection_url()

    test_app, test_container = create_app(test_db_url)
    test_container.init_resources()

    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('sqlalchemy.url', test_db_url)
    command.upgrade(alembic_cfg, 'head')

    with TestClient(test_app) as test_client:
        yield AppTestContext(test_client, test_container)


@pytest.fixture(scope='session')
def client(client_and_container):
    return client_and_container.client


@pytest.fixture(scope='session')
def container(client_and_container):
    return client_and_container.container


@pytest.fixture(autouse=True)
def clean_database(container):
    engine = container.engine()

    metadata = MetaData()
    metadata.reflect(bind=engine)

    with engine.connect() as conn:
        with conn.begin():
            conn.execute(text("SET session_replication_role = 'replica';"))

            for table in reversed(metadata.sorted_tables):
                conn.execute(table.delete())

            conn.execute(text("SET session_replication_role = 'origin';"))


@pytest.fixture
def db_session(container):
    engine = container.engine()
    session = Session(engine)
    yield session
    session.close()
