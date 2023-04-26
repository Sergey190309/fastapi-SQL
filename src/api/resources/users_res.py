from fastapi import (APIRouter, HTTPException)
# from sqlalchemy.ext.asyncio import AsyncSession
from src.api.sqlalchemy_models import models
from src.api.validation_models import schemas
from src.api.crud import user_crud
# from ..db.init_db import get_session

router = APIRouter()


@router.get("/", response_model=list[schemas.User])
async def read_users() -> list[models.User]:
    users = await user_crud.get_users()
    return users


@router.post('/', response_model=schemas.User)
async def create_user(user: schemas.UserCreate) -> models.User | None:
    existing_user = await user_crud.get_user_by_email(email=user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, detail='This email already registered.')
    created_user = await user_crud.create_user(user=user)
    return created_user


@router.delete('/', response_model=schemas.User)
async def delete_user(user_id: int) -> models.User | None:
    existing_user = await user_crud.get_user_by_id(user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f'User with id {user_id} not found.')
    await user_crud.delete_user_by_id(existing_user)
    return existing_user


@router.put("/", response_model=schemas.User)
async def update_user(
        incoming_user: schemas.UserUpdate) -> models.User:
    if incoming_user.email:
        user_by_email = await user_crud.get_user_by_email(
            incoming_user.email)
        if user_by_email:
            raise HTTPException(
                status_code=400,
                detail='User with planned email already registered')
    user = await user_crud.get_user(user_id=incoming_user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    outbound_user = await user_crud.update_user(
        user=user, incoming_user=incoming_user)
    # print('\nusers_res>update_user\n',
    #       'outbound_user ->', outbound_user, '\n',
    #       )
    return outbound_user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int) -> models.User:
    user = await user_crud.get_user(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/{user_id}/items/", response_model=schemas.Item)
async def create_item_for_user(
        user_id: int, item: schemas.ItemCreate) -> models.Item:
    existing_user = await user_crud.get_user_by_id(user_id=user_id)
    if not existing_user:
        raise HTTPException(
            status_code=404, detail=f'User with id {user_id} not found.')
    item = await user_crud.create_user_item(
        incoming_item=item, user_id=user_id)
    return item
