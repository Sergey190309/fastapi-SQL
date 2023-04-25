from sqlalchemy import select
from api.db.init_db import async_session
from api.sqlalchemy_models import models


async def get_items() -> list[models.Item]:
    async with async_session() as session:
        stmt = select(models.Item)
        query_result = await session.execute(stmt)
    return query_result.scalars().all()


async def item_by_id(item_id: int) -> models.Item | None:
    async with async_session() as session:
        stmt = select(models.Item).where(
            models.Item.id == item_id)
        query_result = await session.execute(stmt)
    return query_result.scalars().first()
