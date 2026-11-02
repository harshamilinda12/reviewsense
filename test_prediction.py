from src.predict import predict_sentiment

reviews = [
    "This movie was fantastic. I loved every minute.",
    "acting was terrible and the story was boring.",
    "The movie was okay, but nothing special."
]

for review in reviews:
    result=predict_sentiment(review)
    print("\nReview:", review)
    print("Predicted Sentiment:", result["sentiment"])
    print("Probabilities:", result["probabilities"])
    