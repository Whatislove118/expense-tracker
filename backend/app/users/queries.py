import uuid
from dataclasses import dataclass

from app.cqrs.base import BaseQuery


@dataclass
class GetUserByEmailQuery(BaseQuery):
    email: str


@dataclass
class GetUserByIdQuery(BaseQuery):
    user_id: uuid.UUID
