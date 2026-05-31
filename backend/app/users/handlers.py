from fastapi import HTTPException, status

from app.cqrs.base import CommandHandler, QueryHandler
from app.models.user import User
from app.repositories.user import UserRepository
from app.core.security import hash_password
from app.users.commands import CreateUserCommand
from app.users.queries import GetUserByEmailQuery, GetUserByIdQuery


class CreateUserHandler(CommandHandler["CreateUserCommand", User]):
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def handle(self, command: CreateUserCommand) -> User:
        existing = await self._repo.get_by_email(command.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
        return await self._repo.create(
            name=command.name,
            email=command.email,
            hashed_password=hash_password(command.password),
        )


class GetUserByEmailHandler(QueryHandler["GetUserByEmailQuery", User | None]):
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def handle(self, query: GetUserByEmailQuery) -> User | None:
        return await self._repo.get_by_email(query.email)


class GetUserByIdHandler(QueryHandler["GetUserByIdQuery", User | None]):
    def __init__(self, repo: UserRepository) -> None:
        self._repo = repo

    async def handle(self, query: GetUserByIdQuery) -> User | None:
        return await self._repo.get_by_id(query.user_id)
