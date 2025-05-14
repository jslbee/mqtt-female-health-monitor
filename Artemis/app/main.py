from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from typing import Dict, List
from sqlalchemy.orm import Session
import time

from app.database import get_db
from app.models import SensorTemperature, SensorHeartrate, MenstrualCycle, Prediction
from app.schemas import TemperatureResponse, HeartrateResponse, MenstrualResponse, PredictionResponse

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ---- JWT & 密码管理 ----
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---- 内存用户表 ----
users: Dict[str, str] = {}

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_token(username: str):
    return jwt.encode({"sub": username, "exp": time.time() + 3600}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# ---- 路由 ----
@app.get("/")
def read_root():
    return {"message": "Artemis"}

@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[form_data.username] = get_password_hash(form_data.password)
    return {"msg": "User registered in memory"}

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    hashed = users.get(form_data.username)
    if not hashed or not verify_password(form_data.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": create_token(form_data.username), "token_type": "bearer"}

@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"msg": f"Hello {user}, this is protected"}

# ---- 加了认证的接口 ----
@app.get("/temperature", response_model=List[TemperatureResponse])
def get_temperature(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SensorTemperature).filter(SensorTemperature.user_ID == 1).all()

@app.get("/heartrate", response_model=List[HeartrateResponse])
def get_heartrate(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(SensorHeartrate).filter(SensorHeartrate.user_ID == 1).all()

@app.get("/menstrual", response_model=List[MenstrualResponse])
def get_menstrual(user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(MenstrualCycle).filter(MenstrualCycle.user_ID == 1).all()

@app.get("/prediction/{prediction_id}", response_model=PredictionResponse)
def get_prediction(prediction_id: int, user: str = Depends(get_current_user), db: Session = Depends(get_db)):
    result = db.query(Prediction).filter(Prediction.prediction_id == prediction_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return result
