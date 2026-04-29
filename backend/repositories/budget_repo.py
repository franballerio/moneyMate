from typing import List, Optional
from datetime import datetime
from decimal import Decimal
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

from models.budget import Budget

logger = logging.getLogger(__name__)


class BudgetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        category: str,
        limit_amount: Decimal,
        period: str = "monthly",
    ) -> Budget:
        budget = Budget(
            id=f"{category}_{period}",
            category=category,
            limit_amount=limit_amount,
            period=period,
        )
        self.db.add(budget)
        self.db.commit()
        self.db.refresh(budget)
        logger.info(f"Created budget for category: {category}")
        return budget

    def get_by_id(self, budget_id: str) -> Optional[Budget]:
        return self.db.query(Budget).filter(Budget.id == budget_id).first()

    def get_by_category(self, category: str) -> Optional[Budget]:
        return self.db.query(Budget).filter(Budget.category == category).first()

    def get_all(self) -> List[Budget]:
        return self.db.query(Budget).all()

    def update(
        self,
        budget_id: str,
        limit_amount: Optional[Decimal] = None,
        period: Optional[str] = None,
    ) -> Optional[Budget]:
        budget = self.get_by_id(budget_id)
        if not budget:
            return None

        if limit_amount is not None:
            budget.limit_amount = limit_amount
        if period is not None:
            budget.period = period

        budget.updated_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(budget)
        logger.info(f"Updated budget: {budget_id}")
        return budget

    def delete(self, budget_id: str) -> bool:
        budget = self.get_by_id(budget_id)
        if not budget:
            return False

        self.db.delete(budget)
        self.db.commit()
        logger.info(f"Deleted budget: {budget_id}")
        return True