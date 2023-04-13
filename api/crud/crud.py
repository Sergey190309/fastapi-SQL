# function working with database
from sqlalchemy import select
from sqlalchemy.orm import Session


from ..sqlalchemy_models import models
from ..validation_models import schemas

# session = Session()


def get_user(db: Session, user_id: int) -> models.User:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User:
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(
        session: Session, skip: int = 0, limit: int = 100) -> [models.User]:
    selected = select(models.User)
    result = session.execute(selected)
    # result = session.execute(selected)
    print('\n\nseleced ->', selected, '\n',
          'result ->', result, '\n',
          )
    return result.scalars().all()
    # return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(
        email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100) -> models.Item:
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(
        db: Session, item: schemas.ItemCreate, user_id: int) -> models.Item:
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
