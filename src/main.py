from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

# Allow ChatGPT to talk to our local server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict to https://chat.openai.com
    allow_methods=["*"],
    allow_headers=["*"],
)

NWS_API_URL = "https://api.weather.gov"
HEADERS = {
    "User-Agent": "MyWeatherApp (contact@example.com)",
    "Accept": "application/json"
}


@app.get("/get-forecast")
def get_weather_forecast(lat: float, lon: float):

    # Step 1: Get the Grid ID and Coordinates
    points_url = f"{NWS_API_URL}/points/{lat},{lon}"
    response = requests.get(points_url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Location not supported by NWS (US locations only).")

    point_data = response.json()
    properties = point_data.get("properties", {})

    forecast_url = properties.get("forecast")
    if not forecast_url:
        raise HTTPException(status_code=404, detail="Forecast URL not found.")

    # Step 2: Fetch the actual forecast
    forecast_response = requests.get(forecast_url, headers=HEADERS)
    if forecast_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast.")

    return forecast_response.json()
