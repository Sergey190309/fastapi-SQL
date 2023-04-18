# import asyncio
# import typer
from fastapi import FastAPI
# from sqlalchemy.orm import Session

from .db.init_db import (
    # engine,
    database)
# from .sqlalchemy_models.models import Base
from .resources import items_res
from .resources import users_res


# models.Base.metadata.create_all(engine)

app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


# @app.on_event("startup")
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


app.include_router(users_res.router, prefix='/users', tags=['users'])
app.include_router(items_res.router, prefix='/items', tags=['items'])
