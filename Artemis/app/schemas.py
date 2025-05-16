from pydantic import BaseModel
from datetime import datetime

# 温度数据响应模型
class TemperatureCreate(BaseModel):
    id: int
    timestamp: datetime
    temperature: float
    warning: str | None = None  # 新增字段
    trend: str | None = None    # 新增字段

    class Config:
        orm_mode = True

# 心率数据响应模型
class HeartRateCreate(BaseModel):
    id: int
    timestamp: datetime
    heart_rate: float
    health_status: str

    class Config:
        orm_mode = True

# 经期数据响应模型
class MenstrualCreate(BaseModel):
    id: int
    timestamp: datetime  # 修改为 timestamp
    duration: float      # 修改为 duration
    condition: str       # 修改为 condition，保持一致

    class Config:
        orm_mode = True
