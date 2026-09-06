from typing import Optional, List
from pydantic import BaseModel


class QueryResult(BaseModel):
    activity: Optional[str] = None
    intent: Optional[str] = None
    crop: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    location: Optional[str] = None

    latitude: Optional[float] = None
    longitude: Optional[float] = None

    confidence: float = 0.0

    missing_fields: List[str] = []
    is_valid: bool = False
    message: Optional[str] = None