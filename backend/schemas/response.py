from typing import Any, Optional
from datetime import datetime
from pydantic import BaseModel


class APIResponse(BaseModel):
    success: bool = True
    data: Optional[Any] = None
    error: Optional[str] = None
    timestamp: str = datetime.utcnow().isoformat() + "Z"


class ErrorResponse(BaseModel):
    success: bool = False
    data: Optional[Any] = None
    error: str
    timestamp: str = datetime.utcnow().isoformat() + "Z"