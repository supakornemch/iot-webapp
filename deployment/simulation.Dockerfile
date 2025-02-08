FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application code
COPY scripts/ ./scripts/

ENV API_URL=http://api:8000

CMD ["python", "./scripts/simulate_sensor.py"]
