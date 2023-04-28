# Set up databases
import os
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    # AsyncSession,
    create_async_engine,
    async_sessionmaker
    )
from sqlalchemy.pool import NullPool

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, poolclass=NullPool, echo=True)


class Base(DeclarativeBase):
    pass
# Base = declarative_base()


# async_session = async_sessionmaker(engine)
async_session = async_sessionmaker(engine, expire_on_commit=False)


# Dependency
# async def get_session() -> AsyncSession:
#     async with async_session() as session:
#         yield session
