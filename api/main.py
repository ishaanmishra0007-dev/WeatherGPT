from datetime import date

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator

from ai.query_service import understand_query
from ai.llm_service import generate_ai_explanation
from backend.main import recommendation
from backend.decision_engine.activities import ACTIVITIES 
from backend.alerts.database import initialize_database

initialize_database()
app = FastAPI(
    title="WeatherGPT AI API",
    description="WeatherGPT conversational decision intelligence API",
    version="1.0.0",
)


class QueryRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Natural language weather question",
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
        description="User latitude",
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
        description="User longitude",
    )

    @field_validator("message")
    @classmethod
    def validate_message(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError("Message cannot be empty")

        return value


@app.get("/")
def root():
    return {
        "message": "WeatherGPT AI API is running"
    }


@app.post("/query")
def process_query(request: QueryRequest):

    # 1. Understand the user's natural-language query
    query = understand_query(
        message=request.message,
        latitude=request.latitude,
        longitude=request.longitude,
    )

    # 2. If the query is incomplete, ask for clarification
    if not query.is_valid:
        return {
            "status": "NEEDS_CLARIFICATION",
            "query": query.model_dump(),
            "message": query.message,
        }

    # 3. GPS coordinates are required for weather recommendations
    if query.latitude is None or query.longitude is None:
        return {
            "status": "LOCATION_REQUIRED",
            "query": query.model_dump(),
            "message": "Please allow location access so I can check the weather for your location.",
        }

    # 4. Make sure the requested activity exists
    if query.activity not in ACTIVITIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported activity: {query.activity}",
        )

    # 5. Ask the existing Decision Engine for the recommendation
    try:
        result = recommendation(
            latitude=query.latitude,
            longitude=query.longitude,
            activity=query.activity,
            target_date=date.fromisoformat(query.date),
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Recommendation error: {str(e)}",
        )

    # 6. Extract the actual recommendation
    recommendation_data = result.get("recommendation")

    if not recommendation_data:
        return {
            "status": "NO_RECOMMENDATION",
            "query": query.model_dump(),
            "recommendation": result,
        }

    # 7. Convert Decision Engine reasons into text
    reasons = recommendation_data.get("reasons", [])

    if isinstance(reasons, list):
        reason_text = " ".join(str(reason) for reason in reasons)
    else:
        reason_text = str(reasons)

    # 8. Generate a natural-language explanation
    explanation = generate_ai_explanation(
        activity=recommendation_data.get("activity"),
        crop=query.crop,
        score=recommendation_data.get("score"),
        risk=recommendation_data.get("risk"),
        best_time=recommendation_data.get("best_time"),
        reason=reason_text,
    )

    # 9. Return the complete WeatherGPT response
    return {
        "status": "SUCCESS",
        "query": query.model_dump(),
        "recommendation": recommendation_data,
        "explanation": explanation,
        "alert": result.get("alert"),
        "recommendation_changed": result.get("changed"),
    }