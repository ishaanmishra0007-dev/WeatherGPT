import os

from ai.response_generator import generate_explanation


def generate_ai_explanation(
    activity,
    crop=None,
    score=None,
    risk=None,
    best_time=None,
    reason=None
):
    """
    Generate a natural-language explanation.

    If an LLM is configured, it can be used for the explanation.
    Otherwise, the rule-based explanation generator is used.
    """

    api_key = os.getenv("LLM_API_KEY")

    if not api_key:
        return generate_explanation(
            activity=activity,
            crop=crop,
            score=score,
            risk=risk,
            best_time=best_time,
            reason=reason
        )

    # LLM integration will be added here.
    # For now, use the reliable rule-based fallback.

    return generate_explanation(
        activity=activity,
        crop=crop,
        score=score,
        risk=risk,
        best_time=best_time,
        reason=reason
    )