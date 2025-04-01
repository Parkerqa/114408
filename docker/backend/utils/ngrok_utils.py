import requests
import time
import os

def get_ngrok_url():
    time.sleep(3)
    try:
        res = requests.get("http://ngrok:4040/api/tunnels")
        tunnels = res.json().get("tunnels", [])
        for tunnel in tunnels:
            if tunnel["proto"] == "https":
                return tunnel["public_url"]
    except Exception as e:
        print("無法取得 ngrok URL:", e)
    return None

def set_line_webhook(public_url):
    webhook_url = f"{public_url}/callback"
    access_token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    body = {
        "endpoint": webhook_url
    }

    response = requests.put(
        "https://api.line.me/v2/bot/channel/webhook/endpoint",
        headers=headers,
        json=body
    )

    if response.status_code == 200:
        print(f"✅ Webhook 已設定為：{webhook_url}")
    else:
        print(f"❌ 設定 webhook 失敗，狀態碼: {response.status_code}")
        print(response.text)