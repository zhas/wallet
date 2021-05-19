from fastapi import FastAPI
from fastapi.responses import JSONResponse

from wallet.db import init_db
from wallet.api.v1.endpoints import router as v1_router
from wallet.exceptions import WalletException


def get_application():
    app = FastAPI()

    app.state._db = init_db()

    @app.on_event("startup")
    async def connect():
        await app.state._db.connect()

    @app.on_event("shutdown")
    async def disconnect():
        await app.state._db.disconnect()

    @app.exception_handler(WalletException)
    async def exception_handler(request, exc: WalletException):
        return JSONResponse({"message": str(exc)}, status_code=exc.status_code)

    app.include_router(v1_router, prefix="/v1")

    return app


app = get_application()

