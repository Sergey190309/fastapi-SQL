# function working with database
# from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


from ..sqlalchemy_models import models
# from ..validation_models import schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(
        session: AsyncSession, email: str) -> models.User:
    query_result = await session.execute(select(models.User).where(
        models.User.email == email))
    result = query_result.first()
    # print('\n------>crud>get_user_by_email\n',
    #       'result ->', result, '\n',
    #       )
    return result


async def get_users(
        session: AsyncSession(),
        skip: int = 0, limit: int = 100) -> [models.User]:
    selected = select(models.User)
    result = await session.execute(selected)
    # result = session.execute(selected)
    print('\n\nseleced ->', selected, '\n',
          'result ->', result, '\n',
          )
    return result.scalars().all()
    # return db.query(models.User).offset(skip).limit(limit).all()


# async def create_user(
#         session: AsyncSession(), user: schemas.UserCreate) -> models.User:
#     fake_hashed_password = user.password + "notreallyhashed"
#     db_user = models.User(
#         email=user.email, hashed_password=fake_hashed_password,
#         )
#     session.add(db_user)
#     await session.commit()
#     return db_user


# async def get_items(session: AsyncSession, skip: int = 0, limit: int = 100):
#     # query = select(models.Item)
#     query = select(models.Item).offset(skip).limit(limit)
#     query_result = await session.execute(query)
#     result = query_result.all()
#     # print('\n----->crud>get_items\n',
#     #       'query ->', query, '\n',
#     #       )
#     return result


# def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
#     db_item = models.Item(**item.dict(), owner_id=user_id)
#     db.add(db_item)
#     db.commit()
#     db.refresh(db_item)
#     return db_item
