# function working with database
# from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..sqlalchemy_models import models
from ..validation_models import schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(session: AsyncSession(), email: str):
    return await session.query(
        models.User).filter(models.User.email == email).first()


# def get_users(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.User).offset(skip).limit(limit).all()
async def get_users(
        session: AsyncSession(),
        skip: int = 0, limit: int = 100) -> [models.User]:
    selected = select(models.User)
    result = await session.execute(selected)
    # result = session.execute(selected)
    # print('\n\nseleced ->', selected, '\n',
    #       'result ->', result, '\n',
    #       )
    return result.scalars().all()
    # return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(
        session: AsyncSession(), user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return await db_user


# def get_items(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(models.Item).offset(skip).limit(limit).all()


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
