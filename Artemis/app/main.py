from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Dict

from .database import get_db
from .models import TemperatureData, HeartRateData, MenstrualCycle
from .schemas import TemperatureCreate, HeartRateCreate, MenstrualCreate
from .auth import get_password_hash, verify_password, create_access_token
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://120.76.249.191:8080", 
    "*" 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许的前端地址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# 内存用户字典（不会持久化）
users: Dict[str, str] = {}

# 注册（动态，不写入数据库）
@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[form_data.username] = get_password_hash(form_data.password)
    return {"msg": "User registered in memory"}

# 登录，颁发 token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    hashed = users.get(form_data.username)
    if not hashed or not verify_password(form_data.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_access_token({"sub": form_data.username}), "token_type": "bearer"}

# token 解析验证
def get_current_user(token: str = Depends(oauth2_scheme)):
    from app.auth import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Artemis"}

@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"msg": f"Hello {user}, this is protected."}

@app.get("/temperature", response_model=List[TemperatureCreate])
def get_temperature(db: Session = Depends(get_db)):
    temperatures = db.query(TemperatureData).order_by(TemperatureData.time_received.desc()).limit(10).all()
    return [TemperatureCreate(
        id=temp.id,
        timestamp=temp.time_received,
        temperature=temp.value,
        warning=temp.warning,
        trend=temp.trend
    ) for temp in temperatures]

@app.get("/heartrate", response_model=List[HeartRateCreate])
def get_heartrate(db: Session = Depends(get_db)):
    heart_rates = db.query(HeartRateData).order_by(HeartRateData.time_received.desc()).limit(10).all()
    return [HeartRateCreate(
        id=hr.id,
        timestamp=hr.time_received,
        heart_rate=hr.heart_rate,
        health_status=hr.health_status
    ) for hr in heart_rates]

@app.get("/menstrual", response_model=List[MenstrualCreate])
def get_menstrual(db: Session = Depends(get_db)):
    menstrual_cycles = db.query(MenstrualCycle).order_by(MenstrualCycle.time_received.desc()).limit(10).all()
    return [MenstrualCreate(
        id=mc.id,
        timestamp=mc.time_received,
        duration=mc.duration,
        condition=mc.condition1
    ) for mc in menstrual_cycles]