from core.response import make_response
from fastapi import APIRouter
from schemas.openai import ChatRequest
from views.openai import chat_with_gpt_logic
from starlette.exceptions import HTTPException

openai_router = APIRouter()

@openai_router.post("/chat", summary="Chat with ChatGPT", description="輸入 prompt，取得 ChatGPT 回覆")
async def chat_api(request: ChatRequest):
    reply = chat_with_gpt_logic(request.prompt)
    if not reply:
        raise HTTPException(status_code=500, detail="交談失敗")
    return make_response("成功交談", data={"reply": reply})