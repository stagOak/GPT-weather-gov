from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
from pathlib import Path
import json
from datetime import datetime

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

    # get the grid id and coordinates
    points_url = f"{NWS_API_URL}/points/{lat},{lon}"
    response = requests.get(points_url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Location not supported by NWS (US locations only).")

    point_data = response.json()
    properties = point_data.get("properties", {})

    forecast_url = properties.get("forecast")
    if not forecast_url:
        raise HTTPException(status_code=404, detail="Forecast URL not found.")

    # fetch the actual forecast
    forecast_response = requests.get(forecast_url, headers=HEADERS)
    if forecast_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast.")

    # save forcast response
    # get the directory where script is running
    script_dir = Path(__file__).resolve().parent

    # create the file name and create the file path
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")
    file_path = script_dir.parent / "data/processed" / filename

    # write the response data
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(forecast_response.json(), file, indent=4)

    return forecast_response.json()
