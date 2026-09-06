import re
from datetime import datetime, timedelta

from ai.schemas import QueryResult


ACTIVITY_KEYWORDS = {
    "spraying": [
        "spray",
        "spraying",
        "sprayed",
        "pesticide",
        "pesticides",
        "apply pesticide",
        "apply pesticides",
        "chemical spray",
        "crop spray",
        "spray the crop",
        "spray my crop"
    ],

    "irrigation": [
        "irrigate",
        "irrigation",
        "irrigating",
        "water my crop",
        "water the crop",
        "water my field",
        "watering",
        "water the field"
    ],

    "cricket": [
        "cricket",
        "play cricket",
        "playing cricket"
    ],

    "football": [
        "football",
        "play football",
        "playing football"
    ],

    "driving": [
        "drive",
        "driving",
        "drive my car",
        "car journey",
        "road trip"
    ],

    "trekking": [
        "trek",
        "trekking",
        "hike",
        "hiking",
        "go hiking",
        "go trekking"
    ]
}

CROP_KEYWORDS = {
    "tomato": [
        "tomato",
        "tomatoes",
        "tomato crop",
        "tomato plants"
    ],

    "wheat": [
        "wheat",
        "wheat crop",
        "wheat field"
    ],

    "rice": [
        "rice",
        "rice crop",
        "paddy",
        "paddy crop"
    ],

    "maize": [
        "maize",
        "corn",
        "maize crop",
        "corn crop"
    ],

    "potato": [
        "potato",
        "potatoes",
        "potato crop"
    ],

    "sugarcane": [
        "sugarcane",
        "sugar cane",
        "sugarcane crop"
    ],

    "cotton": [
        "cotton",
        "cotton crop"
    ],

    "mustard": [
        "mustard",
        "mustard crop"
    ]
}


def detect_activity(text: str):
    text = text.lower()

    for activity, keywords in ACTIVITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return activity

    return None

def detect_intent(text: str):
    text = text.lower()

    if any(phrase in text for phrase in [
        "when should",
        "when can",
        "best time",
        "good time",
        "best time to"
    ]):
        return "best_time"

    if any(phrase in text for phrase in [
        "can i",
        "is it okay",
        "is it safe",
        "should i"
    ]):
        return "suitability"

    if any(phrase in text for phrase in [
        "will it rain",
        "weather",
        "forecast"
    ]):
        return "weather"

    return "general"


def detect_crop(text: str):
    text = text.lower()

    for crop, keywords in CROP_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                return crop

    return None


def detect_date(text: str):
    text = text.lower().strip()

    today = datetime.now().date()

    # Day after tomorrow
    if "day after tomorrow" in text:
        return (today + timedelta(days=2)).isoformat()

    # Tomorrow
    if "tomorrow" in text:
        return (today + timedelta(days=1)).isoformat()

    # Today
    if "today" in text:
        return today.isoformat()

    # Weekend
    if "this weekend" in text or "weekend" in text:
        days_until_saturday = (5 - today.weekday()) % 7
        saturday = today + timedelta(days=days_until_saturday)
        return saturday.isoformat()

    # Days of the week
    weekdays = {
        "monday": 0,
        "tuesday": 1,
        "wednesday": 2,
        "thursday": 3,
        "friday": 4,
        "saturday": 5,
        "sunday": 6
    }

    for day_name, day_number in weekdays.items():

        if day_name in text:

            days_ahead = (day_number - today.weekday()) % 7

            # If the requested day is today,
            # interpret it as the next occurrence.
            if days_ahead == 0:
                days_ahead = 7

            target_date = today + timedelta(days=days_ahead)

            return target_date.isoformat()

    return None


def detect_time(text: str):
    text = text.lower()

    # Exact time such as 7 PM or 7:30 AM
    exact_time_pattern = r"\b(\d{1,2})(?::(\d{2}))?\s?(am|pm)\b"

    match = re.search(exact_time_pattern, text)

    if match:
        hour = match.group(1)
        minute = match.group(2)
        period = match.group(3).upper()

        if minute:
            return f"{hour}:{minute} {period}"

        return f"{hour} {period}"

    # General time periods
    if "early morning" in text:
        return "early_morning"

    if "morning" in text:
        return "morning"

    if "noon" in text:
        return "noon"

    if "afternoon" in text:
        return "afternoon"

    if "evening" in text:
        return "evening"

    if "night" in text:
        return "night"

    return None


def detect_location(text: str):
    """
    Location should normally come from the user's
    GPS/device location rather than being guessed
    from the natural-language query.
    """
    return None

def calculate_confidence(
    activity,
    intent,
    crop,
    date,
    time
):
    score = 0.0

    # Activity is the most important field
    if activity is not None:
        score += 0.30

    # Intent
    if intent is not None and intent != "general":
        score += 0.15

    # Date
    if date is not None:
        score += 0.25

    # Time
    if time is not None:
        score += 0.10

    # Crop
    if crop is not None:
        score += 0.20

    return round(min(score, 1.0), 2)

def generate_clarification(missing_fields):
    """
    Generate a user-friendly clarification message
    based on the information missing from the query.
    """

    if not missing_fields:
        return "Query understood successfully."

    questions = {
        "activity": "What activity are you planning to do?",
        "crop": "Which crop are you planning to work with?",
        "date": "Which date are you interested in?"
    }

    messages = []

    for field in missing_fields:
        if field in questions:
            messages.append(questions[field])

    return " ".join(messages)

def parse_query(text: str) -> QueryResult:

    if not text or not text.strip():
        return QueryResult(
            missing_fields=["activity", "date"],
            is_valid=False,
            message="Please provide an activity and date."
        )

    activity = detect_activity(text)
    intent = detect_intent(text)
    crop = detect_crop(text)
    date = detect_date(text)
    time = detect_time(text)
    location = detect_location(text)

    missing_fields = []

    if activity is None:
        missing_fields.append("activity")

    if date is None:
        missing_fields.append("date")

    agricultural_activities = [
        "spraying",
        "irrigation"
    ]

    if activity in agricultural_activities and crop is None:
        missing_fields.append("crop")

    is_valid = len(missing_fields) == 0

    confidence = calculate_confidence(
        activity,
        intent,
        crop,
        date,
        time
    )

    if is_valid:
        message = "Query understood successfully."
    else:
        message = generate_clarification(missing_fields)

    return QueryResult(
        activity=activity,
        intent=intent,
        crop=crop,
        date=date,
        time=time,
        location=location,
        confidence=confidence,
        missing_fields=missing_fields,
        is_valid=is_valid,
        message=message
    )


if __name__ == "__main__":

    query = input("Enter your weather question: ")

    result = parse_query(query)

    print("\nQuery Understanding Result:")
    print(result.model_dump_json(indent=4))