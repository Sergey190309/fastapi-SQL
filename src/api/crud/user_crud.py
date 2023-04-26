# Functions working with database
from sqlalchemy import select
from sqlalchemy.orm import selectinload
# from sqlalchemy.ext.asyncio import AsyncSession


from src.api.db.init_db import async_session
from src.api.sqlalchemy_models import models
from src.api.validation_models import schemas
from src.api.crud.item_crud import item_by_id


async def get_user(user_id: int) -> models.User | None:
    async with async_session() as session:
        stmt = select(models.User).where(models.User.id == user_id).options(
            selectinload(models.User.items))
        query_result = await session.execute(stmt)
    return query_result.scalars().first()


async def get_user_by_email(email: str) -> models.User | None:
    async with async_session() as session:
        stmt = select(models.User).where(models.User.email == email).options(
            selectinload(models.User.items))
        query_result = await session.execute(stmt)
    return query_result.scalars().first()


async def get_user_by_id(user_id: int) -> models.User | None:
    async with async_session() as session:
        stmt = select(models.User).where(models.User.id == user_id).options(
            selectinload(models.User.items))
        query_result = await session.execute(stmt)
    return query_result.scalars().first()


async def delete_user_by_id(user: models.User) -> None:
    # user_to_delete = get_user_by_id(user_id=user_id)
    async with async_session() as session:
        async with session.begin():
            await session.delete(user)
            # session.commit()


async def get_users() -> list[models.User]:
    async with async_session() as session:
        stmt = select(models.User).options(selectinload(models.User.items))
        query_result = await session.execute(stmt)
        # result = query_result.scalars().all()
    # print('\n\nseleced ->', selected, '\n',
    #       'result ->', result, '\n',
    #       )
    return query_result.scalars().all()
    # return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    async with async_session() as session:
        async with session.begin():
            session.add(models.User(email=user.email,
                        hashed_password=fake_hashed_password))
        user = await get_user_by_email(email=user.email)
    return user


async def update_user(
        user: schemas.User, incoming_user: schemas.UserUpdate) -> models.User:
    update_dict = {k: v for k, v in incoming_user.__dict__.items()
                   if v is not None}
    async with async_session() as session:
        async with session.begin():
            stmt = select(models.User).where(
                models.User.id == update_dict.get('id')).options(
                    selectinload(models.User.items))
            query_result = await session.execute(stmt)
            user = query_result.scalars().first()
            for k, v in update_dict.items():
                setattr(user, k, v)
    return user


async def create_user_item(
        incoming_item: schemas.ItemCreate, user_id: int) -> models.Item:
    item = models.Item(**incoming_item.dict(), owner_id=user_id)
    async with async_session() as session:
        async with session.begin():
            session.add(item)
        created_item = await item_by_id(item_id=item.id)
    return created_item
