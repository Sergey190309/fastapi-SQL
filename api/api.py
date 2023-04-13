from fastapi import FastAPI
# from sqlalchemy.orm import Session

from .sqlalchemy_models import models
from .db.init_db import engine
from .resources import items_res
from .resources import users_res

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users_res.router, prefix='/users', tags=['users'])
app.include_router(items_res.router, prefix='/items', tags=['items'])
