from fastapi import FastAPI, Depends

from wallet.dependencies import get_db
from wallet.db import init_db
from wallet import schemas
from wallet import services


def get_application():
    app = FastAPI()

    app.state._db = init_db()

    @app.on_event("startup")
    async def connect():
        await app.state._db.connect()

    @app.on_event("shutdown")
    async def disconnect():
        await app.state._db.disconnect()

    return app


app = get_application()


@app.post("/user/", status_code=201)
async def create_user(user: schemas.User, db=Depends(get_db)):
    user_id = await services.create_user(db, user)
    return user_id
