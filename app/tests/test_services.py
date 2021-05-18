import pytest
from decimal import Decimal

from wallet.services import create_user, create_wallet, make_deposit, make_transfer
from wallet.schemas import User
from wallet.models import users, wallets, deposits, transfers
from wallet.exceptions import UserExists, WalletExists, InsufficientBalance

from sqlalchemy import select

pytestmark = pytest.mark.asyncio

from sqlalchemy.sql.expression import func


async def test_create_user(db, client):
    user = User(username="pete")

    user_id = await create_user(db, user)
    assert user_id is not None

    # check user created
    users_count = await db.execute(
        select([func.count()]).select_from(users)
    )

    assert users_count == 1

    # check user exists
    with pytest.raises(UserExists):
        await create_user(db, user)


async def test_create_wallet(db, client):
    user_id = await db.execute(users.insert().values(username="pete"))

    wallet_id = await create_wallet(db, user_id)

    assert wallet_id is not None

    #  check wallet created
    res = await db.fetch_all(select([wallets.c.balance]))

    assert len(res) == 1
    assert res[0]['balance'] == 0

    #  check wallet exists
    with pytest.raises(WalletExists):
        await create_wallet(db, user_id)


async def test_make_deposit(db, client):
    user_id = await db.execute(users.insert().values(username="pete"))
    wallet_id = await db.execute(wallets.insert().values(owner_id=user_id, balance=0))
    await make_deposit(db, wallet_id, Decimal(150.5))

    # check balance updated
    balance = await db.execute(select([wallets.c.balance]))

    assert balance == 150.5

    # check logs
    res = await db.fetch_one(select([deposits]))
    assert res['wallet_id'] == wallet_id
    assert res['amount'] == 150.5


async def test_make_transfer(db, client):
    user_id = await db.execute(users.insert().values(username="pete"))
    wallet_id = await db.execute(wallets.insert().values(owner_id=user_id, balance=70))
    user2_id = await db.execute(users.insert().values(username="jack"))
    wallet2_id = await db.execute(wallets.insert().values(owner_id=user2_id, balance=30))

    new_balance_1, new_balance_2 = await make_transfer(db, wallet_id, wallet2_id, Decimal(50))

    # check returned balances right
    assert new_balance_1 == 20
    assert new_balance_2 == 80

    # check returned balances right
    res = await db.fetch_all(select([wallets.c.id, wallets.c.balance]))
    res_dict = {r['id']: r['balance'] for r in res}
    assert res_dict[wallet_id] == 20
    assert res_dict[wallet2_id] == 80

    # check logs
    res = await db.fetch_one(select([transfers]))
    assert res['src_id'] == wallet_id
    assert res['dest_id'] == wallet2_id
    assert res['amount'] == 50

    # check insufficient balance
    with pytest.raises(InsufficientBalance):
        await make_transfer(db, wallet_id, wallet2_id, Decimal(100))
