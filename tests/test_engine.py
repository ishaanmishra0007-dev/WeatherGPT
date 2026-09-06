from decision_engine.scorer import calculate_score, get_risk
from decision_engine.optimizer import find_best_hour, find_best_window
from decision_engine.explanation import generate_reasons

weather_data = [
    {
        "time": "07:00",
        "temperature": 24,
        "rain_probability": 5,
        "wind_speed": 7,
        "humidity": 65
    },

    {
        "time": "08:00",
        "temperature": 26,
        "rain_probability": 10,
        "wind_speed": 8,
        "humidity": 62
    },

    {
        "time": "09:00",
        "temperature": 28,
        "rain_probability": 15,
        "wind_speed": 10,
        "humidity": 60
    },

    {
        "time": "10:00",
        "temperature": 31,
        "rain_probability": 20,
        "wind_speed": 13,
        "humidity": 55
    },

    {
        "time": "11:00",
        "temperature": 34,
        "rain_probability": 40,
        "wind_speed": 17,
        "humidity": 50
    }
]

results=[] 
for weather in weather_data:

    score = calculate_score(weather)

    risk = get_risk(score)

    result = {
        "time": weather["time"],
        "score": score,
        "risk": risk
    }

    results.append(result)

    print(
        weather["time"],
        "→ Score:",
        score,
        "Risk:",
        risk
    )

best_hour = find_best_hour(results)

print("\nBest time:", best_hour["time"])
print("Best score:", best_hour["score"])
print("Risk:", best_hour["risk"])
best_window = find_best_window(results, minimum_score=80)

if best_window:

    print(
        "Best window:",
        best_window["start"],
        "to",
        best_window["end"]
    )

    print(
        "Duration:",
        best_window["duration"],
        "hours"
    )

else:

    print("No suitable time window found.")
    best_weather = max(
    weather_data,
    key=lambda x: calculate_score(x)
)
best_weather = max(
    weather_data,
    key=lambda x: calculate_score(x)
)
reasons = generate_reasons(best_weather)

print("\nWhy this time is recommended:")

for reason in reasons:
    print("✓", reason)