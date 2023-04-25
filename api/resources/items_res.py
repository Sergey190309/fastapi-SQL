from fastapi import (APIRouter,
                     HTTPException
                     )

from api.sqlalchemy_models import models
from api.validation_models import schemas
from api.crud import item_crud

router = APIRouter()


@router.get('/', response_model=list[schemas.Item])
async def read_items() -> list[models.Item]:
    items = await item_crud.get_items()
    return items


@router.get('/{item_id}', response_model=schemas.Item)
async def read_item_by_id(item_id: int) -> models.Item:
    item = await item_crud.item_by_id(item_id=item_id)
    if not item:
        raise HTTPException(
            status_code=404,
            detail=f'Item with id {item_id} does not found.')
    return item
