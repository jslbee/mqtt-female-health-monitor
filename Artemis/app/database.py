# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:Artemis452458!@localhost/yourdatabase"

# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"charset": "utf8mb4"})  # 适应 utf8mb4 字符集

# 创建 sessionmaker，用于生成 Session 实例
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建 Base 类，用于映射模型类
Base = declarative_base()

# 依赖项：每次请求创建和关闭数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
