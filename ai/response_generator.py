def generate_explanation(
    activity,
    crop=None,
    score=None,
    risk=None,
    best_time=None,
    reason=None
):
    """
    Generate a natural-language explanation
    from the decision engine result.
    """

    if crop:
        subject = f"your {crop} crop"
    else:
        subject = f"your {activity.replace('_', ' ')} activity"

    parts = []

    if best_time:
        parts.append(
            f"The most suitable time for {subject} is {best_time}."
        )

    if score is not None:
        parts.append(
            f"The suitability score is {score} out of 100."
        )

    if risk:
        parts.append(
            f"The current risk level is {risk.lower()}."
        )

    if reason:
        parts.append(reason)

    if not parts:
        return "I could not generate a recommendation from the available information."

    return " ".join(parts)