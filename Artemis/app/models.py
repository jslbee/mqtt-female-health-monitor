from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

class SensorTemperature(Base):
    __tablename__ = 'sensor_temperature'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    value = Column(Float)
    timestamp = Column(DateTime)

class SensorHeartrate(Base):
    __tablename__ = 'sensor_heartrate'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    value = Column(Float)
    timestamp = Column(DateTime)

class MenstrualCycle(Base):
    __tablename__ = 'menstrual_cycle'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Prediction(Base):
    __tablename__ = 'prediction'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    prediction_result = Column(String(100))
    timestamp = Column(DateTime)
