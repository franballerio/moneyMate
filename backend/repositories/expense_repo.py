from typing import List, Optional, Tuple
from datetime import date, datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import logging

from models.expense import Expense

logger = logging.getLogger(__name__)


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        item: str,
        amount: Decimal,
        category: str,
        date_value: Optional[date] = None,
        created_by: str = "web",
    ) -> Expense:
        expense = Expense(
            item=item,
            amount=amount,
            category=category,
            date=date_value or date.today(),
            created_by=created_by,
            version=1,
        )
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        logger.info(f"Created expense: {expense.id}")
        return expense

    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        return (
            self.db.query(Expense)
            .filter(
                and_(
                    Expense.id == expense_id,
                    Expense.deleted_at.is_(None),
                )
            )
            .first()
        )

    def get_all(
        self,
        page: int = 1,
        limit: int = 20,
        category: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> Tuple[List[Expense], int]:
        query = self.db.query(Expense).filter(Expense.deleted_at.is_(None))

        if category:
            query = query.filter(Expense.category == category)
        if start_date:
            query = query.filter(Expense.date >= start_date)
        if end_date:
            query = query.filter(Expense.date <= end_date)

        total = query.count()
        expenses = (
            query.order_by(Expense.date.desc())
            .offset((page - 1) * limit)
            .limit(limit)
            .all()
        )

        return expenses, total

    def get_by_date(self, date_value: date) -> List[Expense]:
        return (
            self.db.query(Expense)
            .filter(
                and_(
                    Expense.date == date_value,
                    Expense.deleted_at.is_(None),
                )
            )
            .order_by(Expense.date.desc())
            .all()
        )

    def get_by_category(self, category: str) -> List[Expense]:
        return (
            self.db.query(Expense)
            .filter(
                and_(
                    Expense.category == category,
                    Expense.deleted_at.is_(None),
                )
            )
            .order_by(Expense.date.desc())
            .all()
        )

    def get_by_month_year(self, year: int, month: int) -> List[Expense]:
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1)
        else:
            end_date = date(year, month + 1, 1)

        return (
            self.db.query(Expense)
            .filter(
                and_(
                    Expense.date >= start_date,
                    Expense.date < end_date,
                    Expense.deleted_at.is_(None),
                )
            )
            .order_by(Expense.date.desc())
            .all()
        )

    def get_total_by_category(self, category: str) -> Decimal:
        result = (
            self.db.query(func.sum(Expense.amount))
            .filter(
                and_(
                    Expense.category == category,
                    Expense.deleted_at.is_(None),
                )
            )
            .scalar()
        )
        return result if result else Decimal("0")

    def get_total_all(self) -> Decimal:
        result = (
            self.db.query(func.sum(Expense.amount))
            .filter(Expense.deleted_at.is_(None))
            .scalar()
        )
        return result if result else Decimal("0")

    def get_category_totals(self) -> List[Tuple[str, Decimal]]:
        results = (
            self.db.query(Expense.category, func.sum(Expense.amount))
            .filter(Expense.deleted_at.is_(None))
            .group_by(Expense.category)
            .all()
        )
        return results

    def get_daily_totals(self, days: int = 30) -> List[Tuple[date, Decimal]]:
        from datetime import timedelta

        start_date = date.today() - timedelta(days=days)
        results = (
            self.db.query(Expense.date, func.sum(Expense.amount))
            .filter(
                and_(
                    Expense.date >= start_date,
                    Expense.deleted_at.is_(None),
                )
            )
            .group_by(Expense.date)
            .order_by(Expense.date)
            .all()
        )
        return results

    def update(
        self,
        expense_id: int,
        item: Optional[str] = None,
        amount: Optional[Decimal] = None,
        category: Optional[str] = None,
        date_value: Optional[date] = None,
    ) -> Optional[Expense]:
        expense = self.get_by_id(expense_id)
        if not expense:
            return None

        if item is not None:
            expense.item = item
        if amount is not None:
            expense.amount = amount
        if category is not None:
            expense.category = category
        if date_value is not None:
            expense.date = date_value

        expense.version += 1
        expense.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(expense)
        logger.info(f"Updated expense: {expense_id}")
        return expense

    def delete(self, expense_id: int) -> bool:
        expense = self.get_by_id(expense_id)
        if not expense:
            return False

        expense.deleted_at = datetime.utcnow()
        self.db.commit()
        logger.info(f"Soft deleted expense: {expense_id}")
        return True