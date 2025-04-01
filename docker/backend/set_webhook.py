from utils.ngrok_utils import get_ngrok_url, set_line_webhook

if __name__ == "__main__":
    public_url = get_ngrok_url()
    if public_url:
        set_line_webhook(public_url)
    else:
        print("❌ 無法取得 ngrok 公開網址，請確認 ngrok 是否有開啟")