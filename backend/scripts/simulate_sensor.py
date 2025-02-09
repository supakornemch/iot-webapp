import os
import requests
import time
import random
from datetime import datetime
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = os.getenv('API_URL', 'http://localhost:8000')

def create_session():
    session = requests.Session()
    retry_strategy = Retry(
        total=5,
        backoff_factor=2,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def wait_for_api():
    session = create_session()
    max_attempts = 10
    attempt = 0
    
    while attempt < max_attempts:
        try:
            response = session.get(f"{BASE_URL}/docs")
            if response.status_code == 200:
                print("API is ready")
                return True
        except Exception as e:
            print(f"Waiting for API... (attempt {attempt + 1}/{max_attempts})")
        attempt += 1
        time.sleep(5)
    return False

def generate_sensor_data():
    """Generate random sensor data with occasional anomalies"""
    # Normal ranges
    temp_base = 25.0
    humidity_base = 60.0
    air_quality_base = 100.0
    
    # Randomly introduce anomalies (10% chance)
    is_anomaly = random.random() < 0.1
    
    if is_anomaly:
        # Generate anomalous values
        temperature = temp_base + random.uniform(-10, 10)
        humidity = humidity_base + random.uniform(-20, 20)
        air_quality = air_quality_base + random.uniform(-50, 100)
    else:
        # Generate normal values with small variations
        temperature = temp_base + random.uniform(-3, 3)
        humidity = humidity_base + random.uniform(-10, 10)
        air_quality = air_quality_base + random.uniform(-30, 30)
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "temperature": round(temperature, 2),
        "humidity": round(humidity, 2),
        "air_quality": round(air_quality, 2)
    }

def simulate_sensor_data():
    """Continuously send sensor data every second"""
    print("Starting sensor data simulation...")
    print(f"Connecting to API at: {BASE_URL}")
    
    if not wait_for_api():
        print("Failed to connect to API")
        return
    
    session = create_session()
    
    while True:
        try:
            data = generate_sensor_data()
            response = session.post(f"{BASE_URL}/sensor/data", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Sent data: {data}")
                print(f"Anomaly detected: {result['is_anomaly']}\n")
            else:
                print(f"Error sending data: {response.status_code}")
            
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(5)  # Longer delay on error
