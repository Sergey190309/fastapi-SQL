# import asyncio
# import typer
from fastapi import FastAPI
# from sqlalchemy.orm import Session

from src.api.db.init_db import Base, engine
from src.api.resources import users_res, items_res, ping_res


app = FastAPI()


@app.on_event("startup")
async def startup():
    # await database.connect()
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def shutdown():
    pass
    # await database.disconnect()


app.include_router(ping_res.router, prefix='/ping', tags=['ping'])
app.include_router(users_res.router, prefix='/users', tags=['users'])
app.include_router(items_res.router, prefix='/items', tags=['items'])
