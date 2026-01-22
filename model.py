import re
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# ---------------- Download VADER Lexicon ----------------
try:
    nltk.data.find("sentiment/vader_lexicon")
except LookupError:
    nltk.download("vader_lexicon")

# ---------------- Initialize Analyzer ----------------
sia = SentimentIntensityAnalyzer()


def clean_text(text: str) -> str:
    """
    Cleans input text by:
    - Lowercasing
    - Removing URLs
    - Removing numbers and special characters
    - Removing extra spaces
    """
    if not isinstance(text, str):
        return ""

    text = text.lower()
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def analyze_sentiment(text: str) -> str:
    """
    Returns sentiment label only (for backward compatibility)
    """
    score = sia.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"


def analyze_sentiment_with_score(text: str) -> dict:
    """
    Returns sentiment + confidence score
    """
    scores = sia.polarity_scores(text)
    compound = scores["compound"]

    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"

    return {
        "sentiment": sentiment,
        "confidence": round(abs(compound), 3),
        "scores": scores
    }
