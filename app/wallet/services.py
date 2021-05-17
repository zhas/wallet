from wallet import models
from wallet.exceptions import WalletException, WalletNotFound


async def create_user(db, user):
    query = models.users.insert().values(username=user.username)
    user_id = await db.execute(query)
    return user_id


async def create_wallet(username):
    pass


async def transfer_money(src_id, dest_id, amount):
    pass


async def balance_increase(wallet_id, amount):
    pass
