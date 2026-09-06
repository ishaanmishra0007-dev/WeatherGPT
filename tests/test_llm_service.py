from ai.llm_service import generate_ai_explanation


def test_llm_service_fallback():
    result = generate_ai_explanation(
        activity="spraying",
        crop="tomato",
        score=91,
        risk="LOW",
        best_time="7:00 AM - 10:00 AM",
        reason="Rain probability is low and wind conditions are favorable."
    )

    assert result is not None
    assert "tomato" in result.lower()
    assert "91" in result
    assert "7:00 AM - 10:00 AM" in result