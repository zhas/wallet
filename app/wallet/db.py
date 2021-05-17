import os

from databases import Database

DATABASE_URL = os.environ.get("DATABASE_URL")
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")
TESTING = os.environ.get("TESTING") == "1"


def get_db_url():
    if TESTING:
        return TEST_DATABASE_URL
    return DATABASE_URL


def init_db():
    return Database(get_db_url(), force_rollback=TESTING)
