import os

import openai

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