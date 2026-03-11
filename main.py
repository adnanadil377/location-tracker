from fastapi import FastAPI
from fastapi.responses import Response, HTMLResponse
from prometheus_client import Counter, generate_latest
from pydantic import BaseModel
from typing import Optional
import pathlib

app = FastAPI()

# Prometheus metric
REQUEST_COUNT = Counter("gps_requests_total", "Total GPS Requests")
LOCATION_UPDATE_COUNT = Counter("gps_location_updates_total", "Total GPS Location Updates")

# In-memory store for latest real location (falls back to classroom default)
current_location: dict = {
    "latitude": 15.3173,
    "longitude": 75.7139,
    "accuracy": None,
    "source": "default",
    "room": "Network Lab"
}

class LocationUpdate(BaseModel):
    latitude: float
    longitude: float
    accuracy: Optional[float] = None

@app.get("/", response_class=HTMLResponse)
def home():
    html_path = pathlib.Path(__file__).parent / "static" / "index.html"
    return HTMLResponse(content=html_path.read_text(), status_code=200)

@app.get("/location")
def get_location():
    REQUEST_COUNT.inc()
    return current_location

@app.post("/update-location")
def update_location(data: LocationUpdate):
    LOCATION_UPDATE_COUNT.inc()
    current_location["latitude"] = data.latitude
    current_location["longitude"] = data.longitude
    current_location["accuracy"] = data.accuracy
    current_location["source"] = "browser-gps"
    current_location.pop("room", None)
    return {"status": "updated", "location": current_location}

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")