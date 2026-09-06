from fastapi import FastAPI, HTTPException, Query
from datetime import date

from .weather_api import get_weather
from .weather_processor import process_weather
from .decision_engine.analyzer import analyze_day
from .decision_engine.recommendation import generate_recommendation


app = FastAPI(
    title="WeatherGPT API",
    description="Backend API for WeatherGPT",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "WeatherGPT API is running"
    }


@app.get("/recommendation")
def recommendation(
    latitude: float = Query(...),
    longitude: float = Query(...),
    activity: str = Query(...),
    target_date: date = Query(...)
):
    try:
        # 1. Get weather data from Open-Meteo
        weather_data = get_weather(
            latitude,
            longitude
        )

        # 2. Process weather data
        processed_data = process_weather(
            weather_data
        )

        # 3. Analyze the requested day and activity
        results = analyze_day(
            processed_data,
            target_date.strftime("%Y-%m-%d"),
            activity
        )

        # 4. Generate final recommendation
        recommendation_result = generate_recommendation(
            results,
            activity
        )

        return recommendation_result

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Backend error: {str(e)}"
        )