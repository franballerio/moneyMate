from decimal import Decimal
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class BudgetBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=100)
    limit_amount: Decimal = Field(..., gt=0, decimal_places=2)
    period: str = Field(default="monthly", max_length=20)

    @field_validator("period")
    @classmethod
    def validate_period(cls, v):
        if v not in ["monthly", "yearly"]:
            raise ValueError("Period must be 'monthly' or 'yearly'")
        return v


class BudgetCreate(BudgetBase):
    pass


class BudgetUpdate(BaseModel):
    limit_amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    period: Optional[str] = Field(None, max_length=20)


class BudgetResponse(BudgetBase):
    id: str
    created_at: str
    updated_at: str

    model_config = {"from_attributes": True}


class BudgetListResponse(BaseModel):
    items: List[BudgetResponse]
    total: int