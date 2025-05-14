from pydantic import BaseModel
from datetime import datetime

# 温度数据响应模型
class TemperatureResponse(BaseModel):
    id: int
    timestamp: datetime
    temperature: float

    class Config:
        orm_mode = True

# 心率数据响应模型
class HeartrateResponse(BaseModel):
    id: int
    timestamp: datetime
    heartrate: float

    class Config:
        orm_mode = True

# 经期数据响应模型
class MenstrualResponse(BaseModel):
    id: int
    start_date: datetime
    end_date: datetime
    notes: str

    class Config:
        orm_mode = True

# 预测数据响应模型
class PredictionResponse(BaseModel):
    prediction_id: int
    prediction_date: datetime
    result: str

    class Config:
        orm_mode = True
