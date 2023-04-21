# Set up databases
import os
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    AsyncSession, create_async_engine,
    async_sessionmaker
    )

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)


class Base(DeclarativeBase):
    pass
# Base = declarative_base()


# async_session = async_sessionmaker(engine)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Dependency
async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
