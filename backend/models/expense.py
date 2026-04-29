import uuid
from datetime import date, datetime
from sqlalchemy import Column, String, Numeric, Date, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from core.database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    item = Column(String(255), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    category = Column(String(100), nullable=False, index=True)
    date = Column(Date, nullable=False, default=date.today, index=True)
    created_by = Column(String(10), nullable=False, default="web")
    version = Column(Integer, default=1, nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index("idx_expenses_category_date", "category", "date"),
    )

    def __repr__(self):
        return f"<Expense(id={self.id}, item={self.item}, amount={self.amount}, category={self.category})>"