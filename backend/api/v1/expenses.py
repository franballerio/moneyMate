from datetime import date
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
import math

from core.database import get_db
from repositories.expense_repo import ExpenseRepository
from schemas.expense import (
    ExpenseCreate,
    ExpenseUpdate,
    ExpenseResponse,
    ExpenseListResponse,
)
from schemas.response import APIResponse, ErrorResponse

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("", response_model=APIResponse)
def list_expenses(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db),
):
    repo = ExpenseRepository(db)
    expenses, total = repo.get_all(
        page=page,
        limit=limit,
        category=category,
        start_date=start_date,
        end_date=end_date,
    )

    total_pages = math.ceil(total / limit) if limit > 0 else 0

    return APIResponse(
        data=ExpenseListResponse(
            items=[ExpenseResponse.model_validate(e) for e in expenses],
            total=total,
            page=page,
            limit=limit,
            total_pages=total_pages,
        )
    )


@router.get("/{expense_id}", response_model=APIResponse)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    repo = ExpenseRepository(db)
    expense = repo.get_by_id(expense_id)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )

    return APIResponse(data=ExpenseResponse.model_validate(expense))


@router.post("", response_model=APIResponse, status_code=status.HTTP_201_CREATED)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    repo = ExpenseRepository(db)
    created = repo.create(
        item=expense.item,
        amount=expense.amount,
        category=expense.category,
        date_value=expense.date,
        created_by=expense.created_by,
    )

    return APIResponse(data=ExpenseResponse.model_validate(created))


@router.put("/{expense_id}", response_model=APIResponse)
def update_expense(
    expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)
):
    repo = ExpenseRepository(db)
    updated = repo.update(
        expense_id=expense_id,
        item=expense.item,
        amount=expense.amount,
        category=expense.category,
        date_value=expense.date,
    )

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )

    return APIResponse(data=ExpenseResponse.model_validate(updated))


@router.delete("/{expense_id}", response_model=APIResponse)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    repo = ExpenseRepository(db)
    deleted = repo.delete(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with id {expense_id} not found",
        )

    return APIResponse(data={"deleted": True})