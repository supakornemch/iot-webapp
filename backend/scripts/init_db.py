import sys
import os
import pandas as pd
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import SessionLocal, engine
import models

def init_db_from_csv(csv_path: str):
    # Create tables
    models.Base.metadata.create_all(bind=engine)
    
    # Read CSV file
    df = pd.read_csv(csv_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Create DB session
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(models.SensorData).delete()
        
        # Insert records
        for _, row in df.iterrows():
            sensor_data = models.SensorData(
                timestamp=row['timestamp'],
                temperature=row['temperature'] if pd.notna(row['temperature']) else None,
                humidity=row['humidity'] if pd.notna(row['humidity']) else None,
                air_quality=row['air_quality'] if pd.notna(row['air_quality']) else None,
                is_anomaly=False  # Will be updated when querying with anomaly detection
            )
            db.add(sensor_data)
        
        db.commit()
        print(f"Successfully imported {len(df)} records")
        
    except Exception as e:
        print(f"Error importing data: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python init_db.py <path_to_csv>")
        sys.exit(1)
    
    csv_path = sys.argv[1]
    if not os.path.exists(csv_path):
        print(f"Error: File {csv_path} not found")
        sys.exit(1)
    
    init_db_from_csv(csv_path)
