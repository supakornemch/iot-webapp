from fastapi import APIRouter, Depends, HTTPException, Query
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import Optional, List, Dict
from datetime import datetime, timedelta
from pydantic import BaseModel
import numpy as np
import math

from database import get_db
import models
from services import is_anomaly, calculate_aggregates
from enum import Enum

class TimeWindow(str, Enum):
    ONE_MIN = "1m"
    FIVE_MIN = "5m"
    TEN_MIN = "10m"
    FIFTEEN_MIN = "15m"
    THIRTY_MIN = "30m"
    ONE_HOUR = "1h"
    TWO_HOUR = "2h"
    FOUR_HOUR = "4h"
    SIX_HOUR = "6h"
    TWELVE_HOUR = "12h"
    TWENTY_FOUR_HOUR = "24h"

# Request model
class SensorDataIn(BaseModel):
    timestamp: datetime
    temperature: Optional[float]
    humidity: Optional[float] 
    air_quality: Optional[float]

# Response model
class SensorDataOut(BaseModel):
    timestamp: datetime
    temperature: Optional[float]
    humidity: Optional[float]
    air_quality: Optional[float]
    is_anomaly: bool

class PaginatedResponse(BaseModel):
    items: List[Dict]
    total: int
    page: int
    size: int
    total_pages: int

router = APIRouter()

@router.post("/data", response_model=SensorDataOut)
async def ingest_data(data: SensorDataIn, db: Session = Depends(get_db)):
    try:
        # Get recent readings for anomaly detection
        recent = db.query(models.SensorData)\
                  .order_by(desc(models.SensorData.timestamp))\
                  .limit(30)\
                  .all()
        
        # Check for anomalies in each metric
        temp_anomaly = False
        humid_anomaly = False
        air_anomaly = False
        
        if data.temperature is not None:
            recent_temps = [r.temperature for r in recent if r.temperature is not None]
            temp_anomaly = is_anomaly(data.temperature, recent_temps)
            
        if data.humidity is not None:
            recent_humidity = [r.humidity for r in recent if r.humidity is not None]
            humid_anomaly = is_anomaly(data.humidity, recent_humidity)
            
        if data.air_quality is not None:
            recent_air = [r.air_quality for r in recent if r.air_quality is not None]
            air_anomaly = is_anomaly(data.air_quality, recent_air)
        
        # Create database record
        db_record = models.SensorData(
            timestamp=data.timestamp,
            temperature=data.temperature,
            humidity=data.humidity,
            air_quality=data.air_quality,
            is_anomaly=any([temp_anomaly, humid_anomaly, air_anomaly])
        )
        
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        
        return SensorDataOut(
            timestamp=db_record.timestamp,
            temperature=db_record.temperature,
            humidity=db_record.humidity,
            air_quality=db_record.air_quality,
            is_anomaly=db_record.is_anomaly
        )
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

def clean_value(value) -> Optional[float]:
    """Clean and validate float values for JSON serialization"""
    if value is None:
        return None
    try:
        float_val = float(value)
        # Check for invalid float values
        if math.isnan(float_val) or math.isinf(float_val):
            return None
        return float_val
    except (ValueError, TypeError):
        return None

@router.get("/processed", response_model=PaginatedResponse)
def get_processed_data(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(100, ge=1, le=1000, description="Items per page"),
    start_date: Optional[datetime] = Query(None, description="Filter by start date (ISO format)"),
    end_date: Optional[datetime] = Query(None, description="Filter by end date (ISO format)"),
    is_anomaly: Optional[bool] = Query(None, description="Filter by anomaly status"),
    min_temperature: Optional[float] = Query(None, description="Filter by minimum temperature"),
    max_temperature: Optional[float] = Query(None, description="Filter by maximum temperature"),
    min_humidity: Optional[float] = Query(None, description="Filter by minimum humidity"),
    max_humidity: Optional[float] = Query(None, description="Filter by maximum humidity"),
    min_air_quality: Optional[float] = Query(None, description="Filter by minimum air quality"),
    max_air_quality: Optional[float] = Query(None, description="Filter by maximum air quality"),
):
    # Start with base query
    query = db.query(models.SensorData)
    
    # Apply filters
    if start_date:
        query = query.filter(models.SensorData.timestamp >= start_date)
    if end_date:
        query = query.filter(models.SensorData.timestamp <= end_date)
    if is_anomaly is not None:
        query = query.filter(models.SensorData.is_anomaly == is_anomaly)
    if min_temperature is not None:
        query = query.filter(models.SensorData.temperature >= min_temperature)
    if max_temperature is not None:
        query = query.filter(models.SensorData.temperature <= max_temperature)
    if min_humidity is not None:
        query = query.filter(models.SensorData.humidity >= min_humidity)
    if max_humidity is not None:
        query = query.filter(models.SensorData.humidity <= max_humidity)
    if min_air_quality is not None:
        query = query.filter(models.SensorData.air_quality >= min_air_quality)
    if max_air_quality is not None:
        query = query.filter(models.SensorData.air_quality <= max_air_quality)
    
    # Get total count for pagination
    total = query.count()
    total_pages = (total + size - 1) // size
    
    # Apply pagination
    query = query.order_by(models.SensorData.timestamp.desc())\
                 .offset((page - 1) * size)\
                 .limit(size)
    
    # Get data and clean it
    data = query.all()
    cleaned_data = []
    for d in data:
        record = {
            'timestamp': d.timestamp.strftime('%Y-%m-%dT%H:%M:%SZ'),
            'temperature': clean_value(d.temperature),
            'humidity': clean_value(d.humidity),
            'air_quality': clean_value(d.air_quality),
            'is_anomaly': bool(d.is_anomaly)
        }
        cleaned_data.append(record)
    
    return PaginatedResponse(
        items=cleaned_data,
        total=total,
        page=page,
        size=size,
        total_pages=total_pages
    )

@router.get("/aggregated")
def get_aggregated_data(
    window: TimeWindow = Query(
        TimeWindow.ONE_HOUR,
        description="Time window for aggregation"
    ),
    db: Session = Depends(get_db)
):
    time_windows = {
        TimeWindow.ONE_MIN: timedelta(minutes=1),
        TimeWindow.FIVE_MIN: timedelta(minutes=5),
        TimeWindow.TEN_MIN: timedelta(minutes=10),
        TimeWindow.FIFTEEN_MIN: timedelta(minutes=15),
        TimeWindow.THIRTY_MIN: timedelta(minutes=30),
        TimeWindow.ONE_HOUR: timedelta(hours=1),
        TimeWindow.TWO_HOUR: timedelta(hours=2),
        TimeWindow.FOUR_HOUR: timedelta(hours=4),
        TimeWindow.SIX_HOUR: timedelta(hours=6),
        TimeWindow.TWELVE_HOUR: timedelta(hours=12),
        TimeWindow.TWENTY_FOUR_HOUR: timedelta(hours=24)
    }
    
    cutoff = datetime.utcnow() - time_windows[window]
    data = db.query(models.SensorData).filter(models.SensorData.timestamp >= cutoff).all()
    
    if not data:
        # Return empty aggregates if no data found
        return calculate_aggregates(pd.DataFrame(), window)
    
    df = pd.DataFrame([{
        'timestamp': d.timestamp,
        'temperature': float(d.temperature) if d.temperature is not None and not np.isnan(d.temperature) else None,
        'humidity': float(d.humidity) if d.humidity is not None and not np.isnan(d.humidity) else None,
        'air_quality': float(d.air_quality) if d.air_quality is not None and not np.isnan(d.air_quality) else None
    } for d in data])
    
    return calculate_aggregates(df, window)
