from decimal import Decimal
from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class CategoryTotal(BaseModel):
    category: str
    total: Decimal


class TrendData(BaseModel):
    date: str
    total: Decimal


class MetricsSummary(BaseModel):
    daily: Decimal
    monthly: Decimal
    all_time: Decimal


class CategoryBreakdownResponse(BaseModel):
    categories: List[CategoryTotal]
    fx_rate: int = 1500


class TrendsResponse(BaseModel):
    trends: List[TrendData]
    fx_rate: int = 1500