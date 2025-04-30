import os
import openai
from flask import Blueprint, request, jsonify

openai_bp = Blueprint('openai', __name__)

# 初始化 OpenAI 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或 gpt-4
            messages=[
                {"role": "system", "content": "你是一個親切的LINE聊天助手，以下對話請用繁體中文回答問題"},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"ChatGPT 回應失敗：{str(e)}"

# Flask API：用來接收 prompt
@openai_bp.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "缺少 prompt"}), 400

    reply = chat_with_gpt(prompt)
    return jsonify({"reply": reply})