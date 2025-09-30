FROM python:3.10

ENV DEBIAN_FRONTEND=noninteractive

# 安裝必要系統依賴
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libzbar0 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 升級 pip
RUN pip install --upgrade pip

# 安裝 requirements.txt（只裝 CPU Paddle + PaddleOCR）
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

COPY . .

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]