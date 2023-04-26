from typing import List
from sqlalchemy import (
    # Boolean, Column,
    ForeignKey,
    # Integer, String
    )
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..db.init_db import Base


class User(Base):
    __tablename__ = "users_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)

    items: Mapped[List['Item']] = relationship(
        back_populates='user',
        cascade='all, delete-orphan',
        lazy='raise')
    # items: Mapped[List['Item']] = relationship(
    #     back_populates='owner', lazy='raise')


class Item(Base):
    __tablename__ = "items_table"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(index=True)
    description: Mapped[str] = mapped_column(index=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey('users_table.id'))

    user: Mapped['User'] = relationship(back_populates='items')

    # owner: Mapped['User'] =
    # relationship(back_populates="items", lazy='raise')
