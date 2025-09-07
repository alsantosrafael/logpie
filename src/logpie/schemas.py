from pydantic import BaseModel
from typing import Optional, Dict, Any


class LogEntry(BaseModel):
    level: str
    message: str
    context: Optional[Dict[str, Any]] = {}
