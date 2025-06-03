from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Dict
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
from openai import OpenAI

from .database import get_db
from .models import TemperatureData, HeartRateData, MenstrualCycle
from .schemas import TemperatureCreate, HeartRateCreate, MenstrualCreate
from .auth import get_password_hash, verify_password, create_access_token
from .predictor import predict_next_period
from jose import jwt, JWTError
from fastapi.middleware.cors import CORSMiddleware

client = OpenAI(
    api_key="sk-267c35ad9df94b0aa2f1a3bcca60ef09",
    base_url="https://api.deepseek.com/v1"
)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://120.76.249.191:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# In-memory user dictionary (non-persistent)
users: Dict[str, str] = {}

# Register (dynamic, not saved in DB)
@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username in users:
        raise HTTPException(status_code=400, detail="Username already exists")
    users[form_data.username] = get_password_hash(form_data.password)
    return {"msg": "User successfully registered"}

# Login and issue token
@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    hashed = users.get(form_data.username)
    if not hashed or not verify_password(form_data.password, hashed):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": create_access_token({"sub": form_data.username}), "token_type": "bearer"}

# Decode and verify token
def get_current_user(token: str = Depends(oauth2_scheme)):
    from app.auth import SECRET_KEY, ALGORITHM
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/")
def read_root():
    return {"message": "Artemis Health API"}

@app.get("/protected")
def protected(user: str = Depends(get_current_user)):
    return {"msg": f"Hello {user}, this is a protected endpoint."}

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

FIXED_CLIENT_ID = "nfp8122"

class DateRequest(BaseModel):
    last_period_date: str  # Format: YYYY-MM-DD

@app.post("/predict")
def predict(request: DateRequest):
    result = predict_next_period(FIXED_CLIENT_ID, request.last_period_date)
    return {"result": result}

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class Query(BaseModel):
    message: str

@app.post("/chatbot/ask")
def ask_ai(query: Query):
    try:
        user_id = 1
        
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": "You are a gentle and knowledgeable female health assistant. You specialize in answering questions about menstrual cycles, body temperature changes, mood swings, and more. Please respond to users in a calm and concise tone."
                },
                {"role": "user", "content": query.message}
            ],
            temperature=0.7
        )
        answer = response.choices[0].message.content
        return {"response": answer}
    except Exception as e:
        return {"error": str(e)}
