from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import Dict
import time

# 内存中的用户信息（不会持久化）
users: Dict[str, str] = {}

# 密码加密和验证
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# 秘钥和算法
SECRET_KEY = "Artemis452458!"
ALGORITHM = "HS256"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    # 创建 JWT，包含用户名和过期时间
    to_encode = data.copy()
    to_encode.update({"exp": time.time() + 3600})  # 1小时过期
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str) -> str:
    # 解码 token 获取当前用户
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise Exception("Invalid token")
