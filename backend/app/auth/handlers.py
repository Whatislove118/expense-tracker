from fastapi import HTTPException, status

from app.auth.commands import LoginCommand, RegisterCommand
from app.cqrs.base import CommandHandler
from app.cqrs.mediator import Mediator
from app.core.security import create_access_token, create_refresh_token, verify_password
from app.schemas.auth import TokenPair
from app.users.commands import CreateUserCommand
from app.users.queries import GetUserByEmailQuery


class RegisterHandler(CommandHandler["RegisterCommand", TokenPair]):
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def handle(self, command: RegisterCommand) -> TokenPair:
        user = await self._mediator.send(
            CreateUserCommand(name=command.name, email=command.email, password=command.password)
        )
        return TokenPair(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )


class LoginHandler(CommandHandler["LoginCommand", TokenPair]):
    def __init__(self, mediator: Mediator) -> None:
        self._mediator = mediator

    async def handle(self, command: LoginCommand) -> TokenPair:
        user = await self._mediator.send(GetUserByEmailQuery(email=command.email))
        if user is None or not verify_password(command.password, user.hashed_password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        return TokenPair(
            access_token=create_access_token(str(user.id)),
            refresh_token=create_refresh_token(str(user.id)),
        )
