import logging
import os

import openai

logger = logging.getLogger(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

def chat_with_gpt_logic(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # 或 gpt-4
            messages=[
                {"role": "system", "content": "你是一個親切的LINE聊天助手，以下對話請用繁體中文回答問題"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=30,
            timeout = 10
        )
        return response['choices'][0]['message']['content']
    except openai.error.OpenAIError as e:
        logger.warning(f"[OpenAI] 回覆失敗：{e}")
        return False

    except Exception as e:
        logger.error(f"[OpenAI] 未知錯誤：{e}")
        return False

def ocr_correction_logic(prompt: str):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是專門處理發票的資料萃取助手"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=800,
            timeout=10
        )
        return response["choices"][0]["message"]["content"].strip()

    except openai.error.OpenAIError as e:
        print(f"[OpenAI] 回覆失敗：{e}")
        return ""

    except Exception as e:
        print(f"[OpenAI] 未知錯誤：{e}")
        return ""