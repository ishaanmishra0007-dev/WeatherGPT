from .optimizer import find_best_hour, find_best_window
from .explanation import generate_reasons
from .activities import ACTIVITIES
from ..alerts.database import initialize_database, save_recommendation


def generate_recommendation(results, activity="spraying"):

    if not results:
        return {
            "activity": activity,
            "status": "NO_DATA",
            "message": "No weather data available."
        }

    # Find best single hour
    best_hour = find_best_hour(results)

    # Find best continuous window
    activity_config = ACTIVITIES[activity]

    best_window = find_best_window(
        results,
        minimum_score=activity_config["minimum_score"],
        minimum_duration=2
    )

    # Find the weather data for the best hour
    best_weather = None

    for weather in results:

        if weather["time"] == best_hour["time"]:
            best_weather = weather
            break

    # Generate explanation
    reasons = generate_reasons(
    best_weather,
    activity
)

    recommendation = {
        "activity": activity,
        "date": best_hour["date"],
        "best_time": best_hour["time"],
        "score": best_hour["score"],
        "risk": best_hour["risk"],
        "reasons": reasons
    }

    if best_window:

        recommendation["best_window"] = {
            "start": best_window["start"],
            "end": best_window["end"],
            "duration": best_window["duration"],
            "average_score": best_window["average_score"]
        }

    else:

        recommendation["best_window"] = None

    if recommendation.get("status") != "NO_DATA":
        initialize_database()
        save_recommendation(recommendation)

    return recommendation