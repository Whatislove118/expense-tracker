import uuid

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    name: str
    email: EmailStr

    model_config = {"from_attributes": True}
