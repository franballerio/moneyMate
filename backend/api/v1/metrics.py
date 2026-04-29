from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from core.database import get_db
from services.metrics_service import MetricsService
from schemas.metrics import (
    MetricsSummary,
    CategoryBreakdownResponse,
    TrendsResponse,
    CategoryTotal,
    TrendData,
)
from schemas.response import APIResponse

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/summary", response_model=APIResponse)
def get_summary(db: Session = Depends(get_db)):
    service = MetricsService(db)
    summary = service.get_summary()

    return APIResponse(
        data=MetricsSummary(
            daily=summary["daily"],
            monthly=summary["monthly"],
            all_time=summary["all_time"],
        )
    )


@router.get("/categories", response_model=APIResponse)
def get_category_breakdown(db: Session = Depends(get_db)):
    service = MetricsService(db)
    breakdown = service.get_category_breakdown()

    return APIResponse(
        data=CategoryBreakdownResponse(
            categories=[
                CategoryTotal(category=item["category"], total=item["total"])
                for item in breakdown
            ]
        )
    )


@router.get("/trends", response_model=APIResponse)
def get_trends(days: int = Query(30, ge=1, le=365), db: Session = Depends(get_db)):
    service = MetricsService(db)
    trends = service.get_trends(days)

    return APIResponse(
        data=TrendsResponse(
            trends=[
                TrendData(date=item["date"], total=item["total"])
                for item in trends
            ]
        )
    )