import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Download VADER lexicon only once
try:
    nltk.data.find("sentiment/vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon")

# Initialize analyzer
sia = SentimentIntensityAnalyzer()


def clean_text(text: str) -> str:
    """
    Cleans input text by:
    - Lowercasing
    - Removing URLs
    - Removing special characters and numbers
    """
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def analyze_sentiment(text: str) -> str:
    """
    Analyzes sentiment using VADER compound score
    Returns: Positive, Neutral, or Negative
    """
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"
