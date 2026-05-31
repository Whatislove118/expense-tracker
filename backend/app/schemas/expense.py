from decimal import Decimal

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    amount: Decimal
    category: str
    description: str | None = None


class ExpenseRead(BaseModel):
    id: int
    amount: Decimal
    category: str
    description: str | None

    model_config = {"from_attributes": True}
