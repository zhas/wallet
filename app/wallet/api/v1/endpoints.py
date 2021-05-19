from fastapi import Depends
from fastapi import APIRouter

from wallet.deps import get_db
from wallet import schemas, services

router = APIRouter()


@router.post("/user/", status_code=201, response_model=schemas.UserCreateResponse,
             name="wallet:create-user")
async def create_user(inp: schemas.UserCreateRequest, db=Depends(get_db)):
    user_id = await services.create_user(db, inp.username)
    return {"user_id": user_id}


@router.post("/wallet/", status_code=201, response_model=schemas.WalletCreateResponse,
             name="wallet:create-wallet")
async def create_wallet(inp: schemas.WalletCreateRequest, db=Depends(get_db)):
    wallet_id = await services.create_wallet(db, inp.owner_id)
    return {"wallet_id": wallet_id}


@router.post("/wallet/deposit/", status_code=200, response_model=schemas.WalletDepositResponse,
             name="wallet:deposit")
async def make_deposit(inp: schemas.WalletDepositRequest, db=Depends(get_db)):
    balance = await services.make_deposit(db, inp.wallet_id, inp.amount)
    return {"wallet_id": inp.wallet_id, "balance": balance}


@router.post("/wallet/transfer/", status_code=200, response_model=schemas.WalletTransferResponse,
             name="wallet:transfer")
async def make_transfer(inp: schemas.WalletTransferRequest, db=Depends(get_db)):
    src_balance, dest_balance = await services.make_transfer(db, inp.src_id, inp.dest_id,
                                                             inp.amount)
    return {"src_balance": src_balance, "dest_balance": dest_balance}
