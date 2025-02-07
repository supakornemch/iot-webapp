from sqlalchemy import Column, Integer, Float, DateTime, Boolean
from database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    air_quality = Column(Float, nullable=True)
    is_anomaly = Column(Boolean, default=False)
