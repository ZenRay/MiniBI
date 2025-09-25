"""
数据库连接和会话管理模块
"""
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ClickHouse 连接参数
CLICKHOUSE_URL = os.getenv("CLICKHOUSE_URL", "clickhouse")
CLICKHOUSE_PORT = os.getenv("CLICKHOUSE_PORT", "9000")
CLICKHOUSE_USER = os.getenv("CLICKHOUSE_USER", "admin")
CLICKHOUSE_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD", "admin")
CLICKHOUSE_DB = os.getenv("CLICKHOUSE_DB", "bi_mvp")

# 构建连接字符串
CLICKHOUSE_URI = f"clickhouse://{CLICKHOUSE_USER}:{CLICKHOUSE_PASSWORD}@{CLICKHOUSE_URL}:{CLICKHOUSE_PORT}/{CLICKHOUSE_DB}"

# 创建引擎
engine = create_engine(CLICKHOUSE_URI)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 为 ClickHouse 创建特定的基类
metadata = MetaData(bind=engine)
Base = declarative_base(metadata=metadata)

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()