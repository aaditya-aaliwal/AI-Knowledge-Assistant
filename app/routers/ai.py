from fastapi import APIRouter
from app.schemas.ai import AIRequest, AIResponse
from app.services.llm_service import generate_response

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/generate", response_model=AIResponse)
def generate_ai_response(request: AIRequest):
    response = generate_response(request.prompt)
    return AIResponse(response=response)