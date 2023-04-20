from fastapi import (
    APIRouter,
    Depends,
    # HTTPException
    )
from sqlalchemy.ext.asyncio import AsyncSession

# from ..sqlalchemy_models import models
from ..validation_models import schemas
from ..crud import crud
from ..db.init_db import async_session

router = APIRouter()


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
# def get_db():
#     db = async_session()
#     try:
#         yield db
#     finally:
#         db.close()


# @router.post('/', response_model=schemas.User)
# async def create_user(
#         user: schemas.UserCreate,
#         session: AsyncSession() = Depends(get_session)) -> models.User:
#     # db_user = crud.get_user_by_email(db, email=user.email)
#     users = await crud.get_user_by_email(session, email=user.email)
#     # print('\nuser_res>post\n',
#     #       'users ->', users, '\n'
#     #       )
#     if users:
#         raise HTTPException(
#             status_code=400, detail='Email already registered')
#     created_user = await crud.create_user(session=session, user=user)
#     # return created_user
#     return created_user
#     # return await crud.create_user(db=session, user=user)


@router.get("/", response_model=list[schemas.User])
async def read_users(
        skip: int = 0, limit: int = 100,
        sessoin: AsyncSession = Depends(get_session)):
    # print('\n\nuser_res>get\n\n')
    users = await crud.get_users(sessoin, skip=skip, limit=limit)
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
