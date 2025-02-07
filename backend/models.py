from sqlalchemy import Column, Float, DateTime, Integer
from database import Base

class SensorData(Base):
    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime)
    temperature = Column(Float)
    humidity = Column(Float)
    air_quality = Column(Float)
    is_anomaly = Column(Integer, default=0)
