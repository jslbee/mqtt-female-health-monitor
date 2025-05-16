from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
import datetime

class MenstrualCycle(Base):
    __tablename__ = "menstrual_cycle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_received = Column(DateTime, default=datetime.datetime.utcnow)
    duration = Column(Float, nullable=False)
    condition1= Column(String(255), nullable=False)  # condition 字段，保持和 schema 一致

class HeartRateData(Base):
    __tablename__ = "heart_rate_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_received = Column(DateTime, default=datetime.datetime.utcnow)
    heart_rate = Column(Float, nullable=False)
    health_status = Column(String(255), nullable=False)

class TemperatureData(Base):
    __tablename__ = "temperature_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    time_received = Column(DateTime, default=datetime.datetime.utcnow)
    value = Column(Float, nullable=False)
    warning = Column(String(255), nullable=True)  # warning 字段
    trend = Column(String(255), nullable=True)  # trend 字段
