from fastapi import FastAPI
# from sqlalchemy.orm import Session

from .models import models
from .db.database import engine
from .responces import items_resp
from .responces import users_resp

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(users_resp.router, prefix='/users', tags=['users'])
app.include_router(items_resp.router, prefix='/items', tags=['items'])
