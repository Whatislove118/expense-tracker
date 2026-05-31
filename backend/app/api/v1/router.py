from fastapi import APIRouter

from app.api.v1 import auth, expenses, users

router = APIRouter()
router.include_router(auth.router, prefix="/auth", tags=["auth"])
router.include_router(users.router, prefix="/users", tags=["users"])
router.include_router(expenses.router, prefix="/expenses", tags=["expenses"])
