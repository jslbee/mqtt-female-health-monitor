from jose import jwt
from passlib.context import CryptContext
import time

# ---- JWT & 密码管理 ----
SECRET_KEY = "Artemis452458!"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: int = 3600) -> str:
    to_encode = data.copy()
    to_encode.update({"exp": time.time() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
