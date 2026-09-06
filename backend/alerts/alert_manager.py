from .database import get_latest_recommendation, recommendation_changed
from ..decision_engine.recommendation import generate_recommendation


def generate_and_check_alert(results, activity="spraying"):
    old_recommendation = get_latest_recommendation(activity)

    new_recommendation = generate_recommendation(
        results,
        activity
    )

    changed = recommendation_changed(
        old_recommendation,
        new_recommendation
    )

    return {
        "recommendation": new_recommendation,
        "changed": changed
    }