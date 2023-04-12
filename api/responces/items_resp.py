from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..schemas import schemas
from ..crud import crud
from ..db.database import SessionLocal


router = APIRouter()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get('/', response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_items(db, skip=skip, limit=limit)
    return items
