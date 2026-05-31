import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.dependencies import get_current_user_id, get_mediator
from app.cqrs.mediator import Mediator
from app.schemas.user import UserRead
from app.users.queries import GetUserByIdQuery

router = APIRouter()


@router.get("/me", response_model=UserRead)
async def get_me(
    user_id: uuid.UUID = Depends(get_current_user_id),
    mediator: Mediator = Depends(get_mediator),
) -> UserRead:
    user = await mediator.send(GetUserByIdQuery(user_id=user_id))
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
