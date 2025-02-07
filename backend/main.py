from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import sensor
from database import engine
import models

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sensor.router, prefix="/sensor", tags=["sensor"])
