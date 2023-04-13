from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..validation_models import schemas
from ..crud import crud
from ..db.init_db import async_session

router = APIRouter()


# Dependency
def get_db():
    db = async_session()
    try:
        yield db
    finally:
        db.close()


@router.post('/', response_model=schemas.User)
async def create_user(
        user: schemas.UserCreate, db: Session = Depends(get_db)):
    print('\n\nuser_res>post\n\n')
    # db_user = crud.get_user_by_email(db, email=user.email)
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400, detail='Email already registered')
    # created_user = await crud.create_user(db=db, user=user)
    # return created_user
    return await crud.create_user(db=db, user=user)


@router.get("/", response_model=list[schemas.User])
async def read_users(
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    # print('\n\nuser_res>get\n\n')
    users = await crud.get_users(db, skip=skip, limit=limit)
    return users


# @router.get("/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @router.post("/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)
