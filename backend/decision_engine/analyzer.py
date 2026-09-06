from .scorer import calculate_score, get_risk
from .activities import ACTIVITIES


def analyze_day(weather_data, target_date, activity="spraying"):

    if activity not in ACTIVITIES:
        raise ValueError(
            f"Unknown activity: {activity}"
        )

    activity_config = ACTIVITIES[activity]

    weights = activity_config["weights"]
    rules = activity_config["rules"]

    minimum_hour, maximum_hour = activity_config["allowed_hours"]

    results = []

    for weather in weather_data:

        if weather["date"] != target_date:
            continue

        hour = int(weather["time"].split(":")[0])

        # Apply activity-specific time constraint
        if hour < minimum_hour or hour > maximum_hour:
            continue

        score = calculate_score(
            weather,
            weights,
            rules
        )

        risk = get_risk(score)

        result = {
            "date": weather["date"],
            "time": weather["time"],
            "temperature": weather["temperature"],
            "rain_probability": weather["rain_probability"],
            "wind_speed": weather["wind_speed"],
            "humidity": weather["humidity"],
            "score": score,
            "risk": risk
        }

        results.append(result)

    return results