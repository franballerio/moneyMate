from typing import List, Optional
from datetime import date, timedelta
from decimal import Decimal
from sqlalchemy.orm import Session
import logging

from repositories.expense_repo import ExpenseRepository

logger = logging.getLogger(__name__)

FX_RATE: int = 1500


class MetricsService:
    def __init__(self, db: Session):
        self.db = db
        self.expense_repo = ExpenseRepository(db)

    def get_summary(self) -> dict:
        today = date.today()
        current_month = today.month
        current_year = today.year

        daily_expenses = self.expense_repo.get_by_date(today)
        monthly_expenses = self.expense_repo.get_by_month_year(current_year, current_month)
        all_expenses = self.expense_repo.get_all(page=1, limit=100000)[0]

        daily_total = sum(e.amount for e in daily_expenses)
        monthly_total = sum(e.amount for e in monthly_expenses)
        all_time_total = sum(e.amount for e in all_expenses)

        return {
            "daily": daily_total,
            "monthly": monthly_total,
            "all_time": all_time_total,
        }

    def get_category_breakdown(self) -> List[dict]:
        category_totals = self.expense_repo.get_category_totals()
        return [
            {"category": category, "total": total * FX_RATE}
            for category, total in category_totals
        ]

    def get_trends(self, days: int = 30) -> List[dict]:
        daily_totals = self.expense_repo.get_daily_totals(days)
        return [
            {"date": str(day), "total": total * FX_RATE}
            for day, total in daily_totals
        ]

    def apply_fx_rate(self, amount: Decimal) -> Decimal:
        return amount * FX_RATE

    def get_daily_total(self) -> dict:
        today = date.today()
        expenses = self.expense_repo.get_by_date(today)
        total = sum(e.amount for e in expenses)
        return {"total": total * FX_RATE, "date": str(today)}

    def get_monthly_total(self) -> dict:
        today = date.today()
        expenses = self.expense_repo.get_by_month_year(today.year, today.month)
        total = sum(e.amount for e in expenses)
        return {
            "total": total * FX_RATE,
            "month": today.month,
            "year": today.year,
        }

    def get_all_time_total(self) -> dict:
        expenses, _ = self.expense_repo.get_all(page=1, limit=100000)
        total = sum(e.amount for e in expenses)
        return {"total": total * FX_RATE}