import pytest
from starlette.status import (
    HTTP_201_CREATED, HTTP_409_CONFLICT, HTTP_404_NOT_FOUND, HTTP_200_OK,
    HTTP_422_UNPROCESSABLE_ENTITY
)

from wallet.models import users, wallets

pytestmark = pytest.mark.asyncio


async def test_create_user(app, client):
    res = await client.post(
        app.url_path_for("wallet:create-user"), json={"username": "zhas"}
    )
    assert res.status_code == HTTP_201_CREATED

    res = await client.post(
        app.url_path_for("wallet:create-user"), json={"username": "zhas"}
    )
    assert res.status_code == HTTP_409_CONFLICT


async def test_create_wallet(app, db, client):
    user_id = await db.execute(users.insert().values(username="pete"))

    res = await client.post(
        app.url_path_for("wallet:create-wallet"), json={"owner_id": user_id}
    )
    assert res.status_code == HTTP_201_CREATED

    res = await client.post(
        app.url_path_for("wallet:create-wallet"), json={"owner_id": user_id}
    )
    assert res.status_code == HTTP_409_CONFLICT

    res = await client.post(
        app.url_path_for("wallet:create-wallet"), json={"owner_id": 9999}
    )
    assert res.status_code == HTTP_404_NOT_FOUND


async def test_make_deposit(app, db, client):
    user_id = await db.execute(users.insert().values(username="pete"))
    wallet_id = await db.execute(wallets.insert().values(owner_id=user_id, balance=0))

    res = await client.post(
        app.url_path_for("wallet:deposit"), json={"wallet_id": wallet_id, "amount": "77.99"}
    )

    assert res.status_code == HTTP_200_OK

    res = await client.post(
        app.url_path_for("wallet:deposit"), json={"wallet_id": wallet_id, "amount": "77.015"}
    )

    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    res = await client.post(
        app.url_path_for("wallet:deposit"), json={"wallet_id": 9999, "amount": "77.99"}
    )
    assert res.status_code == HTTP_404_NOT_FOUND


async def test_make_transfer(app, db, client):
    user_id = await db.execute(users.insert().values(username="pete"))
    wallet_id = await db.execute(wallets.insert().values(owner_id=user_id, balance=70))
    user2_id = await db.execute(users.insert().values(username="jack"))
    wallet2_id = await db.execute(wallets.insert().values(owner_id=user2_id, balance=30))

    res = await client.post(
        app.url_path_for("wallet:transfer"),
        json={"src_id": wallet_id, "dest_id": wallet2_id, "amount": "20.99"}
    )

    assert res.status_code == HTTP_200_OK

    res = await client.post(
        app.url_path_for("wallet:transfer"),
        json={"src_id": wallet_id, "dest_id": wallet2_id, "amount": "20.999"}
    )

    assert res.status_code == HTTP_422_UNPROCESSABLE_ENTITY

    res = await client.post(
        app.url_path_for("wallet:transfer"),
        json={"src_id": wallet_id, "dest_id": wallet2_id, "amount": "120"}
    )

    assert res.status_code == HTTP_409_CONFLICT

    res = await client.post(
        app.url_path_for("wallet:transfer"),
        json={"src_id": 1234, "dest_id": wallet2_id, "amount": "20"}
    )

    assert res.status_code == HTTP_404_NOT_FOUND
