from datetime import date, datetime
from sqlalchemy import Column, String, Numeric, DateTime, Index
from core.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id = Column(String(100), primary_key=True)
    category = Column(String(100), nullable=False, unique=True, index=True)
    limit_amount = Column(Numeric(12, 2), nullable=False)
    period = Column(String(20), nullable=False, default="monthly")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_budgets_category", "category"),
    )

    def __repr__(self):
        return f"<Budget(category={self.category}, limit={self.limit_amount})>"