import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Ensure VADER lexicon is downloaded silently
try:
    nltk.data.find("sentiment/vader_lexicon.zip")
except LookupError:
    nltk.download("vader_lexicon", quiet=True)


def analyze_headlines_sentiment(scraped_items: list, show_title: str):
    """Calculates VADER sentiment scores for headlines, stripping out the show title

    to prevent lexical word bias.
    """
    sia = SentimentIntensityAnalyzer()
    processed_data = []

    # Prepare regex pattern to strip exact show title words
    escaped_title = re.escape(show_title.strip())
    title_regex = re.compile(escaped_title, re.IGNORECASE)

    for item in scraped_items:
        original_headline = item["headline"]

        # Strip title string out for unbiased VADER evaluation
        cleaned_text = title_regex.sub("", original_headline).strip()
        if not cleaned_text:
            cleaned_text = original_headline

        scores = sia.polarity_scores(cleaned_text)
        compound = scores["compound"]

        # Categorize
        if compound > 0.05:
            sentiment_label = "Positive"
        elif compound < -0.05:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Neutral"

        processed_data.append(
            {
                "headline": original_headline,
                "publisher": item["publisher"],
                "link": item["link"],
                "published": item["published"],
                "compound": compound,
                "pos": scores["pos"],
                "neu": scores["neu"],
                "neg": scores["neg"],
                "sentiment": sentiment_label,
            }
        )

    total_count = len(processed_data)
    if total_count == 0:
        return processed_data, {
            "avg_compound": 0.0,
            "pos_pct": 0.0,
            "neu_pct": 0.0,
            "neg_pct": 0.0,
            "total_items": 0,
        }

    pos_count = sum(1 for d in processed_data if d["sentiment"] == "Positive")
    neg_count = sum(1 for d in processed_data if d["sentiment"] == "Negative")
    neu_count = sum(1 for d in processed_data if d["sentiment"] == "Neutral")

    avg_compound = round(
        sum(d["compound"] for d in processed_data) / total_count, 3
    )

    summary = {
        "avg_compound": avg_compound,
        "pos_pct": round((pos_count / total_count) * 100, 1),
        "neu_pct": round((neu_count / total_count) * 100, 1),
        "neg_pct": round((neg_count / total_count) * 100, 1),
        "total_items": total_count,
    }

    return processed_data, summary