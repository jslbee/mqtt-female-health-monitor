# app/insert_data.py

from sqlalchemy.orm import Session
from .models import MenstrualCycle, HeartRateData, TemperatureData
import datetime

def save_menstrual_data(db: Session, duration: float, condition: str):
    record = MenstrualCycle(
        time_received=datetime.datetime.now(),
        duration=duration,
        condition1=condition
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    print("Menstrual data inserted:", record.id)

def save_heart_rate_data(db: Session, heart_rate: float, health_status: str, timestamp: str):
    record = HeartRateData(
        time_received=timestamp,
        heart_rate=heart_rate,
        health_status=health_status
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    print("Heart rate data inserted:", record.id)

def save_temperature_data(db: Session, value: float, warning: str, trend: str):
    record = TemperatureData(
        time_received=datetime.datetime.now(),
        value=value,
        warning=warning,
        trend=trend
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    print("Temperature data inserted:", record.id)
