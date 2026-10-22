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

    response = chat(
        message=request.message,
        business_id=request.business_id,
        customer_id=request.customer_id,
        history=request.history
    )
    return ChatResponse(
        success=True,
        response=response
    )