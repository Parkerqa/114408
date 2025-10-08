FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# 安裝 Python 3.10 和系統依賴
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3.10 \
    python3.10-venv \
    python3-pip \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libzbar0 \
    && rm -rf /var/lib/apt/lists/*
# 設定 python/pip 預設版本
RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

WORKDIR /app

# 建立獨立的虛擬環境
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 升級 pip
RUN pip install --upgrade pip

RUN pip install paddlepaddle-gpu==3.1.0 -i https://www.paddlepaddle.org.cn/packages/stable/cu118/

# 安裝專案依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案程式碼
COPY . .

# 預設啟動
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]