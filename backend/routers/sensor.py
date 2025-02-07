from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import pandas as pd
from datetime import datetime, timedelta

from database import get_db
import models
from services import clean_and_process_data, calculate_aggregates

router = APIRouter()

@router.post("/data")
async def ingest_data(file: UploadFile, db: Session = Depends(get_db)):
    try:
        df = pd.read_csv(file.file)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Process and clean data
        processed_df = clean_and_process_data(df)
        
        # Save to database
        for _, row in processed_df.iterrows():
            db_record = models.SensorData(
                timestamp=row['timestamp'],
                temperature=row['temperature'],
                humidity=row['humidity'],
                air_quality=row['air_quality'],
                is_anomaly=any([row['temperature_anomaly'], 
                              row['humidity_anomaly'], 
                              row['air_quality_anomaly']])
            )
            db.add(db_record)
        
        db.commit()
        return {"message": "Data ingested successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/processed")
def get_processed_data(db: Session = Depends(get_db)):
    data = db.query(models.SensorData).all()
    df = pd.DataFrame([{
        'timestamp': d.timestamp,
        'temperature': d.temperature,
        'humidity': d.humidity,
        'air_quality': d.air_quality,
        'is_anomaly': d.is_anomaly
    } for d in data])
    return df.to_dict(orient='records')

@router.get("/aggregated")
def get_aggregated_data(window: str = "1h", db: Session = Depends(get_db)):
    time_windows = {
        "10m": timedelta(minutes=10),
        "1h": timedelta(hours=1),
        "24h": timedelta(hours=24)
    }
    
    if window not in time_windows:
        raise HTTPException(status_code=400, detail="Invalid time window")
        
    cutoff = datetime.utcnow() - time_windows[window]
    data = db.query(models.SensorData).filter(models.SensorData.timestamp >= cutoff).all()
    
    df = pd.DataFrame([{
        'timestamp': d.timestamp,
        'temperature': d.temperature,
        'humidity': d.humidity,
        'air_quality': d.air_quality
    } for d in data])
    
    return calculate_aggregates(df, window)
