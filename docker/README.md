# 🎟️ TicketTransformer

> 使用 FastAPI + LINE Bot + MySQL 打造的智慧記帳/發票處理系統。支援 Docker 一鍵部署、ngrok 自動更新 webhook！

---

## 📦 專案結構



---

## 🚀 快速開始

### ✅ 安裝 Docker & Docker Compose（如尚未安裝）

https://docs.docker.com/get-docker/

---

### 🛠 環境變數設定 `.env`

建立 `.env` 檔案並填入以下內容：

```env
# === Backend SETTING ===
DB_HOST=db
DB_PORT=3306
DB_USER=user
DB_PASSWORD=user123456
DB_DATABASE=114408

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN=你的AccessToken
LINE_CHANNEL_SECRET=你的ChannelSecret

# ngrok 設定
NGROK_AUTHTOKEN=你的NgrokToken
```

---

### 🐳 啟動所有服務

```aiignore
(第一次啟動)
docker compose up --build

(之後啟動)
docker compose up
```

### 🗂️ 匯入DataBase

```aiignore
(第一次啟動)
docker compose exec -T db mysql -uroot -p123456 114408 < ./vm_mysql/backup.sql
```