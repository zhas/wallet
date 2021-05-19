from typing import Tuple

from wallet.models import users, wallets, deposits, transfers
from wallet.exceptions import (
    WalletExists, UserExists, InsufficientBalance, UserNotFound, WalletNotFound
)
from databases import Database
from decimal import Decimal
from asyncpg.exceptions import UniqueViolationError, ForeignKeyViolationError
from sqlalchemy import select, update, case


async def create_user(db: Database, username: str) -> int:
    """
    Create user if not exists else raise exception.
    Check uniqueness via insert/catch instead of select/insert,
    because its prevents race conditions.
    """
    async with db.transaction():
        query = users.insert().values(username=username)

        try:
            user_id = await db.execute(query)
        except UniqueViolationError as e:
            if e.constraint_name == "uq_users_username":
                raise UserExists(f"User with username={username} already exists")
            raise
        else:
            return user_id


async def create_wallet(db: Database, owner_id: int) -> int:
    """
    Create wallet if not exists else raise exception
    Check uniqueness via insert/catch instead of select/insert,
    because its prevents race conditions.
    """
    async with db.transaction():
        query = wallets.insert().values(owner_id=owner_id, balance=0)

        try:
            wallet_id = await db.execute(query)
        except UniqueViolationError as e:
            if e.constraint_name == "uq_wallets_owner_id":
                raise WalletExists(f"Wallet with owner_id={owner_id} already exists")
            raise
        except ForeignKeyViolationError as e:
            if e.constraint_name == "fk_wallets_owner_id_users":
                raise UserNotFound(f"User with id={owner_id} not found")
            raise
        else:
            return wallet_id


async def make_deposit(db: Database, wallet_id: int, amount: Decimal) -> Decimal:
    """
    Make deposit to wallet (wallet_id) by some amount (amount).
    """
    async with db.transaction():
        query = (
            update(wallets)
                .where(wallets.c.id == wallet_id)
                .values(balance=(wallets.c.balance + amount))
                .returning(wallets.c.balance)
        )

        new_balance = await db.execute(query)

        try:
            await db.execute(deposits.insert().values(wallet_id=wallet_id, amount=amount))
        except ForeignKeyViolationError as e:
            if e.constraint_name == "fk_deposits_wallet_id_wallets":
                raise WalletNotFound(f"Wallet with id={wallet_id} not found")
            raise
        else:
            return new_balance


async def make_transfer(
        db: Database, src_id: int, dest_id: int, amount: Decimal) -> Tuple[Decimal, Decimal]:
    """
    Make transfer of some amount (amount) from one wallet (src_id) to another wallet (dest_id).
    Check balance and avoid race condition using with_for_update(select for update) feature.
    Return updated balances.
    """
    async with db.transaction():
        query = (
            select([wallets.c.id, wallets.c.balance])
                .with_for_update()
                .where(wallets.c.id.in_([src_id, dest_id]))
        )

        res = await db.fetch_all(query)
        res_dict = {r['id']: r['balance'] for r in res}

        try:
            src_balance, dest_balance = res_dict[src_id], res_dict[dest_id]
        except KeyError as e:
            raise WalletNotFound(f"Wallet with id={e.args[0]} not found")

        if src_balance - amount < 0:
            raise InsufficientBalance(f"Insufficient balance{src_balance} for this operation")

        query = (
            update(wallets)
                .where(wallets.c.id.in_([src_id, dest_id]))
                .values(
                balance=case([
                    (wallets.c.id == src_id, wallets.c.balance - amount),
                    (wallets.c.id == dest_id, wallets.c.balance + amount),
                ])
            )
                .returning(wallets)
        )
        res = await db.fetch_all(query)
        res_dict = {r['id']: r['balance'] for r in res}

        await db.execute(transfers.insert().values(src_id=src_id, dest_id=dest_id, amount=amount))

        return res_dict[src_id], res_dict[dest_id]
