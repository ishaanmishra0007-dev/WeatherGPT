from ai.query_parser import parse_query
from ai.query_service import understand_query


def test_tomato_spraying_tomorrow():
    result = parse_query(
        "When should I spray my tomato crop tomorrow?"
    )

    assert result.activity == "spraying"
    assert result.intent == "best_time"
    assert result.crop == "tomato"
    assert result.date is not None
    assert result.is_valid is True


def test_tomato_spraying_tomorrow_morning():
    result = parse_query(
        "Can I spray my tomato plants tomorrow morning?"
    )

    assert result.activity == "spraying"
    assert result.intent == "suitability"
    assert result.crop == "tomato"
    assert result.time == "morning"
    assert result.date is not None
    assert result.is_valid is True


def test_wheat_irrigation():
    result = parse_query(
        "When should I irrigate my wheat field tomorrow?"
    )

    assert result.activity == "irrigation"
    assert result.intent == "best_time"
    assert result.crop == "wheat"
    assert result.date is not None
    assert result.is_valid is True


def test_cricket_query():
    result = parse_query(
        "Can I play cricket tomorrow at 7 PM?"
    )

    assert result.activity == "cricket"
    assert result.intent == "suitability"
    assert result.date is not None
    assert result.time == "7 PM"
    assert result.is_valid is True


def test_missing_crop():
    result = parse_query(
        "Can I spray tomorrow?"
    )

    assert result.activity == "spraying"
    assert result.crop is None
    assert result.date is not None
    assert "crop" in result.missing_fields
    assert result.is_valid is False


def test_missing_activity():
    result = parse_query(
        "What should I do tomorrow?"
    )

    assert result.activity is None
    assert result.date is not None
    assert "activity" in result.missing_fields
    assert result.is_valid is False


def test_missing_date():
    result = parse_query(
        "When should I spray my tomato crop?"
    )

    assert result.activity == "spraying"
    assert result.crop == "tomato"
    assert result.date is None
    assert "date" in result.missing_fields
    assert result.is_valid is False


def test_day_after_tomorrow():
    result = parse_query(
        "When should I spray my tomato crop day after tomorrow?"
    )

    assert result.activity == "spraying"
    assert result.crop == "tomato"
    assert result.date is not None


def test_monday_query():
    result = parse_query(
        "When should I irrigate my wheat crop on Monday?"
    )

    assert result.activity == "irrigation"
    assert result.crop == "wheat"
    assert result.date is not None


def test_confidence_score():
    result = parse_query(
        "When should I spray my tomato crop tomorrow?"
    )

    assert result.confidence > 0
    assert result.confidence <= 1


def test_clarification_message():
    result = parse_query(
        "Can I spray tomorrow?"
    )

    assert result.is_valid is False
    assert result.message is not None
    assert "crop" in result.message.lower()


def test_service_interface():
    result = understand_query(
        "When should I spray my tomato crop tomorrow?",
        latitude=28.67,
        longitude=77.43
    )

    assert result.activity == "spraying"
    assert result.crop == "tomato"
    assert result.date is not None
    assert result.latitude == 28.67
    assert result.longitude == 77.43
    assert result.is_valid is True