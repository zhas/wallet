import warnings
import os

import pytest
import alembic
from alembic.config import Config
from sqlalchemy_utils import create_database, database_exists
from asgi_lifespan import LifespanManager

from httpx import AsyncClient

os.environ["TESTING"] = "1"


# Apply migrations at beginning and end of testing session
@pytest.fixture(scope="session")
def apply_migrations():
    from wallet.db import get_db_url
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    db_url = get_db_url()

    if not database_exists(db_url):
        create_database(db_url)

    config = Config("alembic.ini")
    alembic.command.upgrade(config, "head")
    yield
    alembic.command.downgrade(config, "base")


# Create a new application for testing
@pytest.fixture
def app(apply_migrations):
    from wallet.main import get_application
    app = get_application()
    return app


# Grab a reference to our database when needed
@pytest.fixture
def db(app):
    return app.state._db


# Make requests in our tests
@pytest.fixture
async def client(app) -> AsyncClient:
    async with LifespanManager(app):
        async with AsyncClient(
                app=app, base_url="http://testserver", headers={"Content-Type": "application/json"}
        ) as client:
            yield client
