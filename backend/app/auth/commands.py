from dataclasses import dataclass

from app.cqrs.base import BaseCommand


@dataclass
class RegisterCommand(BaseCommand):
    name: str
    email: str
    password: str


@dataclass
class LoginCommand(BaseCommand):
    email: str
    password: str
