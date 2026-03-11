from fastapi import FastAPI
from prometheus_client import Counter, generate_latest
from fastapi.responses import Response

app = FastAPI()

# Prometheus metric
REQUEST_COUNT = Counter("gps_requests_total", "Total GPS Requests")

# Example classroom location
CLASSROOM_LOCATION = {
    "latitude": 15.3173,
    "longitude": 75.7139,
    "room": "Network Lab"
}

@app.get("/")
def home():
    return {"message": "GPS Microservice Running"}

@app.get("/location")
def get_location():
    REQUEST_COUNT.inc()
    return CLASSROOM_LOCATION

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")