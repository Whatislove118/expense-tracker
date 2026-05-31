from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.commands import LoginCommand, RegisterCommand
from app.core.dependencies import get_mediator
from app.core.security import create_access_token, create_refresh_token, decode_token
from app.cqrs.mediator import Mediator
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair
from app.schemas.user import UserCreate

router = APIRouter()


@router.post("/register", response_model=TokenPair, status_code=status.HTTP_201_CREATED)
async def register(body: UserCreate, mediator: Mediator = Depends(get_mediator)) -> TokenPair:
    return await mediator.send(RegisterCommand(name=body.name, email=body.email, password=body.password))


@router.post("/login", response_model=TokenPair)
async def login(body: LoginRequest, mediator: Mediator = Depends(get_mediator)) -> TokenPair:
    return await mediator.send(LoginCommand(email=body.email, password=body.password))


@router.post("/refresh", response_model=TokenPair)
async def refresh(body: RefreshRequest) -> TokenPair:
    try:
        payload = decode_token(body.refresh_token)
        if payload.get("type") != "refresh":
            raise ValueError("Not a refresh token")
        subject = payload["sub"]
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token")
    return TokenPair(
        access_token=create_access_token(subject),
        refresh_token=create_refresh_token(subject),
    )
