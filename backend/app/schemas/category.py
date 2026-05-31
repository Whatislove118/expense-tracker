import uuid

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    color: str
    icon: str


class CategoryUpdate(BaseModel):
    name: str | None = None
    color: str | None = None
    icon: str | None = None


class CategoryRead(BaseModel):
    id: uuid.UUID
    name: str
    color: str
    icon: str
    user_id: uuid.UUID

    model_config = {"from_attributes": True}
