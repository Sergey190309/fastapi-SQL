from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class ConfigDict:
        from_attributes = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    id: int
    email: str | None
    is_active: bool | None
    # items: list[Item] | None


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class ConfigDict:
        from_attributes = True
