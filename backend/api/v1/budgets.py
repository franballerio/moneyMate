from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from repositories.budget_repo import BudgetRepository
from schemas.budget import BudgetCreate, BudgetUpdate, BudgetResponse
from schemas.response import APIResponse

router = APIRouter(prefix="/budgets", tags=["budgets"])


@router.get("", response_model=APIResponse)
def list_budgets(db: Session = Depends(get_db)):
    repo = BudgetRepository(db)
    budgets = repo.get_all()

    return APIResponse(
        data={
            "items": [BudgetResponse.model_validate(b) for b in budgets],
            "total": len(budgets),
        }
    )


@router.get("/{budget_id}", response_model=APIResponse)
def get_budget(budget_id: str, db: Session = Depends(get_db)):
    repo = BudgetRepository(db)
    budget = repo.get_by_id(budget_id)

    if not budget:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )

    return APIResponse(data=BudgetResponse.model_validate(budget))


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_budget(budget: BudgetCreate, db: Session = Depends(get_db)):
    repo = BudgetRepository(db)

    existing = repo.get_by_category(budget.category)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Budget for category {budget.category} already exists",
        )

    created = repo.create(
        category=budget.category,
        limit_amount=budget.limit_amount,
        period=budget.period,
    )

    return APIResponse(data=BudgetResponse.model_validate(created))


@router.put("/{budget_id}", response_model=APIResponse)
def update_budget(budget_id: str, budget: BudgetUpdate, db: Session = Depends(get_db)):
    repo = BudgetRepository(db)
    updated = repo.update(
        budget_id=budget_id,
        limit_amount=budget.limit_amount,
        period=budget.period,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )

    return APIResponse(data=BudgetResponse.model_validate(updated))


@router.delete("/{budget_id}", response_model=APIResponse)
def delete_budget(budget_id: str, db: Session = Depends(get_db)):
    repo = BudgetRepository(db)
    deleted = repo.delete(budget_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Budget with id {budget_id} not found",
        )

    return APIResponse(data={"deleted": True})