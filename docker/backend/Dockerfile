FROM python:3.10

# 安裝必要套件，給 OCR (PaddleOCR) 用
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# 設定工作目錄
WORKDIR /app

# 複製 requirements.txt 並安裝 Python 套件
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案
COPY . .

# 啟動 Flask 伺服器
CMD ["python", "app.py"]