from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator

from ai.query_service import understand_query


app = FastAPI(
    title="WeatherGPT API",
    description="API for WeatherGPT natural language query understanding",
    version="1.0.0"
)


class QueryRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        description="Natural language query from the user"
    )

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
        description="User latitude"
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
        description="User longitude"
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
        "message": "WeatherGPT API is running"
    }


@app.post("/query")
def process_query(request: QueryRequest):

    result = understand_query(
        message=request.message,
        latitude=request.latitude,
        longitude=request.longitude
    )

    return result