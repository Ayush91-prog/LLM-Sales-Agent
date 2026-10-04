from pydantic import BaseModel
from typing import Any, List, Optional, Dict

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Dict[str, Any]]] = None

class ChatResponse(BaseModel):
    success: bool
    response: Any