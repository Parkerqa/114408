from fastapi import APIRouter
from pydantic import BaseModel
from utils.openai import chat_with_gpt

router = APIRouter(tags=["OpenAI GPT"])

class ChatRequest(BaseModel):
    prompt: str

@router.post("/chat", summary="Talk with ChatGPT", description="輸入 prompt，取得 ChatGPT 回覆")
async def chat_api(request: ChatRequest):
    reply = chat_with_gpt(request.prompt)
    return {"response": reply}