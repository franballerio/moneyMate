from fastapi import APIRouter
from api.v1 import expenses, budgets, metrics

api_router = APIRouter(prefix="/v1")

api_router.include_router(expenses.router)
api_router.include_router(budgets.router)
api_router.include_router(metrics.router)