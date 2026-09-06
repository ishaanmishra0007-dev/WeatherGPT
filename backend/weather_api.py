import requests


def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "precipitation_probability",
            "wind_speed_10m",
            "relative_humidity_2m"
        ],
        "timezone": "auto"
    }

    response = requests.get(url, params=params)

    response.raise_for_status()

    return response.json()