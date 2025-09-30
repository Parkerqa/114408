FROM nvidia/cuda:12.6.1-cudnn-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y \
    python3 python3-pip python3-dev build-essential \
    libgl1 libglib2.0-0 libsm6 libxrender1 libxext6 libzbar0 \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 升級 pip
RUN python3 -m pip install --upgrade pip

# 安裝 PaddlePaddle GPU (CUDA 12.6 nightly)
RUN pip install --pre --upgrade paddlepaddle-gpu -i https://www.paddlepaddle.org.cn/packages/nightly/cu126/

# 安裝其他依賴
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.org/simple

COPY . .

ENV XLA_FLAGS=--xla_gpu_cuda_data_dir=/usr/local/cuda

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]