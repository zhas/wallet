from pydantic import BaseModel, condecimal
from decimal import Decimal

Money = condecimal(max_digits=12, decimal_places=2)


class UserCreateRequest(BaseModel):
    username: str


class UserCreateResponse(BaseModel):
    user_id: int


class WalletCreateRequest(BaseModel):
    owner_id: int


class WalletCreateResponse(BaseModel):
    wallet_id: int


class WalletDepositRequest(BaseModel):
    wallet_id: int
    amount: Money  # type:ignore


class WalletDepositResponse(BaseModel):
    wallet_id: int
    balance: Decimal


class WalletTransferRequest(BaseModel):
    src_id: int
    dest_id: int
    amount: Money  # type:ignore


class WalletTransferResponse(BaseModel):
    src_balance: Decimal
    dest_balance: Decimal
