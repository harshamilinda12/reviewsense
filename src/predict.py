
import joblib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "sentiment_model.joblib" #path of the model
model = joblib.load(MODEL_PATH) #loading trained model


def predict_sentiment(review: str) -> dict:
    """Predict the sentiment of a given review.
        Args:review: Raw review text.
        Returns:Dictionary containing sentiment and probabilities.
    """
    # Validate input
    if not isinstance(review, str) or not review.strip():
        raise ValueError("Review cannot be empty.")

    # Predict sentiment
    prediction = model.predict([review])[0]

    # Get class probabilities
    probabilities = model.predict_proba([review])[0]

    # Map probabilities to their sentiment labels
    probability_scores = {
        label: round(float(score), 4)
        for label, score in zip(model.classes_, probabilities)
    }

    return {
        "sentiment": prediction,
        "probabilities": probability_scores
    }
#convert prob. for sentiments into a dictionary so the API can return a clean JSON response later.