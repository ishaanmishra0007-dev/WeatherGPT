from ai.response_generator import generate_explanation


def test_spraying_explanation():
    result = generate_explanation(
        activity="spraying",
        crop="tomato",
        score=91,
        risk="LOW",
        best_time="7:00 AM - 10:00 AM",
        reason="Rain probability is low and wind conditions are favorable."
    )

    assert "tomato" in result.lower()
    assert "91" in result
    assert "7:00 AM - 10:00 AM" in result
    assert "low" in result.lower()


def test_activity_without_crop():
    result = generate_explanation(
        activity="cricket",
        score=85,
        risk="LOW",
        best_time="5:00 PM - 7:00 PM",
        reason="Weather conditions are suitable."
    )

    assert "cricket" in result.lower()
    assert "85" in result
    assert "5:00 PM - 7:00 PM" in result


def test_missing_recommendation_data():
    result = generate_explanation(
        activity="spraying"
    )

    assert result is not None
    assert len(result) > 0