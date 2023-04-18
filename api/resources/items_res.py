from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..validation_models import schemas
from ..crud import crud
from ..db.init_db import async_session


router = APIRouter()


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


@router.get('/', response_model=list[schemas.Item])
async def read_items(
        skip: int = 0, limit: int = 100,
        session: AsyncSession = Depends(get_session)):
    items = await crud.get_items(session, skip=skip, limit=limit)
    return items
