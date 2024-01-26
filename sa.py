import wikipedia as wk
from textblob import TextBlob
from collections import Counter
import streamlit as st
import pandas as pd


# Function for Wikipedia Sentiment Analysis
def wiki_sentimental_analysis(url):
    # Get the Wikipedia text content
    text = wk.page(url).content

    # Create a TextBlob object
    blob = TextBlob(text)

    # Perform sentiment analysis
    sentiment_polarity = blob.sentiment.polarity

    # Interpret the sentiment
    if sentiment_polarity > 0:
        sentiment_label = "Positive"
        sentiment_words = [
            {"word": word.lower(), "score": blob.sentiment.polarity, "frequency": count}
            for word, count in Counter(
                [
                    word.lower()
                    for word, score in blob.tags
                    if score == "JJ" and blob.word_counts[word.lower()] > 1
                ]
            ).items()
        ]
    elif sentiment_polarity < 0:
        sentiment_label = "Negative"
        sentiment_words = [
            {"word": word.lower(), "score": blob.sentiment.polarity, "frequency": count}
            for word, count in Counter(
                [
                    word.lower()
                    for word, score in blob.tags
                    if score == "JJ" and blob.word_counts[word.lower()] > 1
                ]
            ).items()
        ]
    else:
        sentiment_label = "Neutral"
        sentiment_words = [
            {"word": word.lower(), "score": blob.sentiment.polarity, "frequency": count}
            for word, count in Counter(
                [
                    word.lower()
                    for word, score in blob.tags
                    if score == "NN" and blob.word_counts[word.lower()] > 1
                ]
            ).items()
        ]

    # Prepare the results
    results = {
        "sentiment_label": sentiment_label,
        "sentiment_polarity": sentiment_polarity,
        "sentiment_words": sentiment_words,
    }

    return results


# Example usage
url = "https://en.wikipedia.org/wiki/Hand_scraper"
sentiment_results = wiki_sentimental_analysis(url)

# Display the sentiment words as a DataFrame
st.write("Sentiment Words:")
sentiment_df = pd.DataFrame(sentiment_results["sentiment_words"])
st.write(sentiment_df)
