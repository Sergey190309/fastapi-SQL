# Functions working with database
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession


from api.db.init_db import async_session
from api.sqlalchemy_models import models
from api.validation_models import schemas


# def get_user(db: Session, user_id: int):
#     return db.query(models.User).filter(models.User.id == user_id).first()


async def get_user_by_email(
        session: AsyncSession, email: str) -> models.User:
    selected = select(models.User).where(models.User.email == email).options(
        selectinload(models.User.items))
    query_result = await session.execute(selected)
    # await session.refresh(query_result)
    result = query_result.first()
    # print('\n------>crud>get_user_by_email\n',
    #       'result ->', result, '\n',
    #       )
    return result


async def get_users(
        session: AsyncSession(),
        skip: int = 0, limit: int = 100) -> [models.User]:
    selected = select(models.User).options(selectinload(models.User.items))
    query_result = await session.execute(selected)
    result = query_result.scalars().all()
    await session.commit()
    # print('\n\nseleced ->', selected, '\n',
    #       'result ->', result, '\n',
    #       )
    return result
    # return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(
        session: AsyncSession(),
        user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    user = models.User(
        email=user.email, hashed_password=fake_hashed_password,
        )

    # async with async_session() as inner_session:
    #     async with inner_session.begin():
    #         inner_session.add(user)

    # await session.refresh(models.User, ['items'])
    session.add(user)
    await session.commit()

    print('\ncrud>create_user\n',
          #   'stmt ->', stmt2, '\n'
          )
    return user


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
