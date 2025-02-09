import json
from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routers import sensor
from database import engine
import models
import threading
from scripts.simulate_sensor import simulate_sensor_data


def start_sensor_simulation():
    simulate_sensor_data()


@asynccontextmanager
async def lifespan(app: FastAPI):
    simulation_thread = threading.Thread(target=start_sensor_simulation, daemon=True)
    simulation_thread.start()
    yield


models.Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(sensor.router, prefix="/sensor", tags=["sensor"])


@app.get("/openapi.yaml", include_in_schema=False)
def get_openapi_yaml():
    openapi_schema = app.openapi()
    json_schema = json.dump(openapi_schema)
    return Response(content=json_schema, media_type="application/json")
