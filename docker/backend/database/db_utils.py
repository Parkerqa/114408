import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 從環境變數讀取資料庫設定
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_DATABASE")

# 建立資料庫連線字串
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 建立 Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,  # 自動檢查連線狀態，避免 MySQL timeout
)

# 建立 Session 工廠
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# 建立 Base
Base = declarative_base()