# 1. 安裝輕量級的 Python
FROM python:3.10-slim

# 設定環境變數
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 限制 Paddle/NumPy 只使用單一執行緒，避免與 Docker 資源競爭導致 Deadlock (卡死)
ENV OMP_NUM_THREADS=1
ENV MKL_NUM_THREADS=1
# 允許 OpenMP 函式庫重複載入 (防止某些情況下的崩潰或靜默失敗)
ENV KMP_DUPLICATE_LIB_OK=TRUE

WORKDIR /app

# 2. 安裝系統依賴
# PP-Structure (OpenCV) 依賴 libgl1, libglib2.0 等圖形庫
# libzbar0 是您原本用到的 (通常用於條碼識別)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgl1 \
    libzbar0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# 3. 升級 pip
RUN pip install --upgrade pip

# 4. 安裝 PaddlePaddle CPU 版
RUN pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

# 5. 安裝專案依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# 6. 複製專案程式碼
COPY . .

# 7. 啟動服務
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]