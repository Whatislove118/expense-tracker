import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decode_token
from app.cqrs.mediator import Mediator
from app.database import get_db

bearer_scheme = HTTPBearer()


async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
) -> uuid.UUID:
    try:
        payload = decode_token(credentials.credentials)
        return uuid.UUID(payload["sub"])
    except (JWTError, KeyError, ValueError):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")


async def get_mediator(session: AsyncSession = Depends(get_db)) -> Mediator:
    from app.repositories.user import UserRepository
    from app.users.commands import CreateUserCommand
    from app.users.queries import GetUserByEmailQuery, GetUserByIdQuery
    from app.users.handlers import CreateUserHandler, GetUserByEmailHandler, GetUserByIdHandler
    from app.auth.commands import RegisterCommand, LoginCommand
    from app.auth.handlers import RegisterHandler, LoginHandler

    mediator = Mediator()
    user_repo = UserRepository(session)

    mediator.register(CreateUserCommand, CreateUserHandler(user_repo))
    mediator.register(GetUserByEmailQuery, GetUserByEmailHandler(user_repo))
    mediator.register(GetUserByIdQuery, GetUserByIdHandler(user_repo))

    mediator.register(RegisterCommand, RegisterHandler(mediator))
    mediator.register(LoginCommand, LoginHandler(mediator))

    return mediator
