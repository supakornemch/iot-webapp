import requests
import time
import random
from datetime import datetime

BASE_URL = "http://localhost:8000"

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
    print("Press Ctrl+C to stop")
    
    while True:
        try:
            data = generate_sensor_data()
            response = requests.post(f"{BASE_URL}/sensor/data", json=data)
            
            if response.status_code == 200:
                result = response.json()
                print(f"Sent data: {data}")
                print(f"Anomaly detected: {result['is_anomaly']}\n")
            else:
                print(f"Error sending data: {response.status_code}")
            
            time.sleep(1)  # Wait for 1 second
            
        except KeyboardInterrupt:
            print("\nStopping simulation...")
            break
        except Exception as e:
            print(f"Error: {str(e)}")
            time.sleep(1)  # Wait before retrying

if __name__ == "__main__":
    simulate_sensor_data()
