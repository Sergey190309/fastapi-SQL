# import asyncio
# import typer
from fastapi import FastAPI
# from sqlalchemy.orm import Session

from .db.init_db import engine, Base
from .sqlalchemy_models import models
from .resources import items_res
from .resources import users_res


# models.Base.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def init_models():
    # print('init_models')
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.drop_all)
        await conn.run_sync(models.Base.metadata.create_all)

# asyncio.run(init_models())


@app.on_event("startup")
async def startup():
    await Base.connect()


@app.on_event("shutdown")
async def shutdown():
    await Base.disconnect()


app.include_router(users_res.router, prefix='/users', tags=['users'])
app.include_router(items_res.router, prefix='/items', tags=['items'])
