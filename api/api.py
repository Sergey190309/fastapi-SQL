from fastapi import FastAPI
# from sqlalchemy.orm import Session

from .db.init_db import engine
from .sqlalchemy_models import models
from .resources import items_res
from .resources import users_res

models.Base.metadata.create_all(engine)

app = FastAPI()


# @app.on_event("startup")
# async def startup():
#     await database.connect()


# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


app.include_router(users_res.router, prefix='/users', tags=['users'])
app.include_router(items_res.router, prefix='/items', tags=['items'])
