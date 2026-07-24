from fastapi import APIRouter

from app.memory.chat_memory import (
    add_ai_message,
    add_user_message,
    get_chat_history,
)
from app.prompts.chat_prompt import (
    CHAT_PROMPT,
    format_instructions,
)
from app.schemas.chat_ai import ChatRequest, ChatResponse
from app.services.llm_service import generate_response


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post(
    "",
    response_model=ChatResponse,
)
def chat(
    request: ChatRequest,
):
    add_user_message(request.message)

    chat_history = get_chat_history()

    prompt = CHAT_PROMPT.format(
        chat_history=chat_history,
        question=request.message,
        format_instructions=format_instructions,
    )

    response = generate_response(prompt)

    add_ai_message(response)

    return ChatResponse(
        response=response,
    )