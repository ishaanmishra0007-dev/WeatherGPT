from datetime import datetime


def process_weather(weather_data):

    hourly = weather_data["hourly"]

    results = []

    for i in range(len(hourly["time"])):

        timestamp = datetime.fromisoformat(
            hourly["time"][i]
        )

        weather = {
            "date": timestamp.strftime("%Y-%m-%d"),
            "time": timestamp.strftime("%H:%M"),
            "temperature": hourly["temperature_2m"][i],
            "rain_probability": hourly["precipitation_probability"][i],
            "wind_speed": hourly["wind_speed_10m"][i],
            "humidity": hourly["relative_humidity_2m"][i]
        }

        results.append(weather)

    return results