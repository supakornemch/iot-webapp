# **IoT Data Processing Assignment**

## **Objective**

Develop a **backend service** that processes IoT time-series data and provides an API to retrieve aggregated insights.

## **Requirements**

### **1. Backend (FastAPI / Django REST Framework)**

- Create an API to **ingest sensor data** (temperature, humidity, air quality).
- Store the data in any **SQL database** (SQLite, PostgreSQL, or MySQL preferred).
- Implement an endpoint to fetch **aggregated insights** (mean, median, min/max over user-defined time windows, e.g., last 10 minutes, 1 hour, 24 hours).

### **2. Data Processing**

- Implement **data cleaning** (remove duplicate values, handle missing data).
- Apply **simple anomaly detection** (Z-score or IQR to flag outliers).
- Return the cleaned dataset through an API endpoint.

### **3. Basic Frontend (Vue 3 + TypeScript)**

- Build a simple page that **fetches processed data** via API.
- Use **any chart library** to display sensor trends.
- Highlight **anomalies** in the visualization.

## **Expected API Endpoints**

```
POST /sensor/data        → Ingest raw sensor data
GET /sensor/processed    → Fetch cleaned & anomaly-detected data
GET /sensor/aggregated   → Fetch aggregated statistics (mean, median, min/max)
```

## **Deliverables**

- **GitHub Repository Link** (preferred) OR ZIP file with the project.
- **README** with setup instructions.
- **API Documentation** (OpenAPI spec or Postman collection).
- **Short explanation (1 paragraph)** on the data cleaning & anomaly detection approach.

## **Recommended Project Structure (You can adjust as needed)**

```
/assignment
├── backend
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   ├── services.py
│   ├── routers
│   │   ├── sensor.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── frontend
│   ├── src
│   │   ├── App.vue
│   │   ├── components
│   │   │   ├── SensorChart.vue
│   │   ├── main.ts
│   ├── package.json
│   ├── vite.config.ts
│   ├── Dockerfile
│
├── README.md
└── docker-compose.yml
```

## **Example Data**

[sensor_data.csv](attachment:4fff4e38-6492-4687-947f-d3f8902b8cd3:sensor_data.csv)

## **Submission Instructions**

- Send an email to **chansric@scg.com** with:
    - **GitHub Repository Link** (preferred) OR ZIP file with the project.
    - **Short explanation** of the data processing approach.
    - **API documentation** (Postman collection or OpenAPI spec).

## **Time Expectation**

- Submit within **48 hours** after receiving the assignment.

---

This assignment is designed to assess your ability to work with **data ingestion, cleaning, anomaly detection, and visualization**. Good luck!