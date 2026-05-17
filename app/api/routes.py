from fastapi import APIRouter
from app.models.api_models import ChatRequest
from app.agent.orchestrator import handle_chat

router = APIRouter()


@router.get("/health")
async def health():
    return {
        "status": "ok"
    }


@router.post("/chat")
async def chat(request: ChatRequest):
    return await handle_chat(request.messages)