from unittest import result

import pytest
from src.predict import predict_sentiment

def test_positive_review():
    result = predict_sentiment("This movie was absolutely fantastic and wonderful.")
    assert result["sentiment"] == "positive"  #Check whether the model predicts positive sentiment.If not the test fails.


def test_negative_review():
    result = predict_sentiment("This movie was terrible and extremely boring.")
    assert result["sentiment"] == "negative"

def test_probabilities_sum_to_one():
    result = predict_sentiment("The movie was really enjoyable.")
    probabilities = result["probabilities"]
    assert abs(sum(probabilities.values()) - 1.0) < 1e-6

def test_empty_review():
    with pytest.raises(ValueError):
        predict_sentiment("")

def test_whitespace_review():
    with pytest.raises(ValueError):
        predict_sentiment("   ")