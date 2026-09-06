from datetime import datetime, timedelta

from weather_api import get_weather
from weather_processor import process_weather

from decision_engine.analyzer import analyze_day
from decision_engine.recommendation import generate_recommendation


# Temporary test location: Ghaziabad
latitude = 28.646748
longitude = 77.48004


# Get real weather
weather_data = get_weather(latitude, longitude)

# Process weather
processed_data = process_weather(weather_data)


# Get tomorrow's date
first_date = datetime.strptime(
    processed_data[0]["date"],
    "%Y-%m-%d"
)

tomorrow = (
    first_date + timedelta(days=1)
).strftime("%Y-%m-%d")


# Analyze tomorrow
results = analyze_day(
    processed_data,
    tomorrow,
    activity="spraying"
)


# Generate final recommendation
recommendation = generate_recommendation(
    results,
    activity="spraying"
)


print("\nWeatherGPT Recommendation")
print("=========================")

print(
    "Activity:",
    recommendation["activity"]
)

print(
    "Date:",
    recommendation["date"]
)

print(
    "Best time:",
    recommendation["best_time"]
)

print(
    "Score:",
    recommendation["score"]
)

print(
    "Risk:",
    recommendation["risk"]
)


if recommendation["best_window"]:

    window = recommendation["best_window"]

    print(
        "Best window:",
        window["start"],
        "to",
        window["end"]
    )

    print(
        "Duration:",
        window["duration"],
        "hours"
    )

    print(
        "Average score:",
        window["average_score"]
    )


print("\nWhy this time is recommended:")

for reason in recommendation["reasons"]:

    print("✓", reason)