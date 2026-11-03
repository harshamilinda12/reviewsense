
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from src.predict import predict_sentiment 

#create FastAPI application
app = FastAPI(title="ReviewSense API",description="An API for predicting sentiment in movie reviews.",
              version="1.0.0"
)

#define the expected input structure

class ReviewRequest(BaseModel):
    review: str = Field(
        ...,
        min_length=3,
        max_length=10000,
        description="Movie review text to analyze"
    )

    @field_validator("review")
    @classmethod
    def validate_review(cls, value):

        # Remove leading and trailing whitespace
        value = value.strip()

        # Check whether the review contains alphabetic characters
        if not any(char.isalpha() for char in value):
            raise ValueError(
                "Review must contain alphabetic characters."
            )

        return value


#define the expected output structure
class SentimentResponse(BaseModel):
    sentiment: Literal["positive", "negative"]
    probabilities: dict[str, float]


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to ReviewSense API",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


# Sentiment prediction endpoint
@app.post("/predict", response_model=SentimentResponse)
def predict(request: ReviewRequest):

    try:
        result = predict_sentiment(request.review)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )
