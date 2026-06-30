from fastapi import APIRouter

from schemas.ai import ChatRequest,ChatResponse
from services.ai_agent import chat

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post(
    "/chat",
    response_model=ChatResponse
)

def chat_with_ai(request:ChatRequest):

    response = chat(request.message)
    return ChatResponse(
        success=True,
        response=response
    )