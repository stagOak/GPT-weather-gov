from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
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
    "User-Agent": "MyWeatherApp (steven.morin@comcast.net)",
    "Accept": "application/json"
}


@app.get("/get-forecast")
def get_weather_forecast(lat: float, lon: float):
    # 1. Get the grid id and coordinates
    points_url = f"{NWS_API_URL}/points/{lat},{lon}"
    response = requests.get(points_url, headers=HEADERS)

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Location not supported by NWS (US locations only).")

    point_data = response.json()
    properties = point_data.get("properties", {})

    forecast_url = properties.get("forecast")
    if not forecast_url:
        raise HTTPException(status_code=404, detail="Forecast URL not found.")

    # 2. Fetch the actual forecast
    forecast_response = requests.get(forecast_url, headers=HEADERS)
    if forecast_response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch forecast.")

    forecast_json = forecast_response.json()

    # 3. Save forecast response (Saves the ENTIRE full-sized data file locally)
    script_dir = Path(__file__).resolve().parent
    filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.json")
    file_path = script_dir.parent / "data/processed" / filename

    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(forecast_json, file, indent=4)

    # 4. FIX: Extract the forecast periods and trim them to bypass the size error
    forecast_periods = forecast_json.get("properties", {}).get("periods", [])

    if not forecast_periods:
        raise HTTPException(status_code=500, detail="Weather data payload missing forecast periods.")

    # Slice the list to only return the first 3 periods (e.g., Today, Tonight, Tomorrow)
    # This keeps your ngrok network traffic tiny, light, and safe from OpenAI's size limit
    trimmed_periods = forecast_periods[:3]

    # Create your custom verification signature
    server_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    verification_message = f"LIVE_VERIFIED_FROM_MY_PROXY_SERVER_AT_{server_time}"

    # Return the clean, ultra-light payload
    return JSONResponse(content={
        "verification_signature": verification_message,
        "periods": trimmed_periods
    })

