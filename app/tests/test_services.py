import pytest

from wallet.services import create_user
from wallet.schemas import User
from wallet.models import users

from sqlalchemy import select

pytestmark = pytest.mark.asyncio

from sqlalchemy.sql.expression import func


async def test_user_create(db, client):
    user = User(username="Pete")

    user_id = await create_user(db, user)
    assert user_id is not None

    users_count = await db.execute(
        select([func.count()]).select_from(users)
    )

    assert users_count == 1
