from dataclasses import dataclass

from app.cqrs.base import BaseCommand


@dataclass
class CreateUserCommand(BaseCommand):
    name: str
    email: str
    password: str
