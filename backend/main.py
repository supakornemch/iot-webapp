import json
from fastapi import FastAPI, Response
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

# Add new OpenAPI YAML endpoint
@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    openapi_schema = app.openapi()
    json_schema = json.dump(openapi_schema)
    return Response(content=json_schema, media_type="application/json")
