import streamlit as sl
import wikipedia as wk
from time import time
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
import pandas as pd

with sl.form("Wiki Search"):
    url = sl.text_input("Enter the Wikipedia page URL")
    url = url.split("/")[-1]
    val = sl.selectbox(
        "Search for",
        options=[
            "Content",
            "Summary",
            "Images",
            "Refrences",
            "Top 10 Most Frequent Words",
            "Sentimental Analysis",
            "All data",
        ],
    )
    submit_btn = sl.form_submit_button("Search")

sl.write("##")


def wiki_content(url):
    text = wk.page(url).content
    text = text.replace("`", "")
    return text


def wiki_summary(url):
    summ = wk.summary(url, sentences=10)
    summ = summ.replace("`", "")
    return summ


def wiki_images(url):
    imgs = wk.page(url)
    img_urls = imgs.images
    return img_urls


def wiki_refrences(url):
    refs = wk.page(url)
    ref_urls = refs.references
    return ref_urls


def freq_words(text):
    words = text.split()
    word_counts = Counter(words)
    top10 = word_counts.most_common(10)
    top10 = sorted(top10, key=lambda x: x[0].lower())
    return top10


def wiki_sentimental_analysis(url):
    text = wk.page(url).content

    blob = TextBlob(text)

    sentiment_polarity = blob.sentiment.polarity

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


def time_taken():
    end = time()
    time_taken = format((end - start), ".2f")
    time_taken = "Searched in " + str(time_taken) + " seconds"
    sl.success(time_taken)


if submit_btn:
    start = time()
    if val == "Content":
        sl.write("## Wikipedia Text:")
        sl.write("##")
        sl.write(wiki_content(url))
        time_taken()
    elif val == "Summary":
        sl.write("## Wikipedia Summary:")
        sl.write("##")
        sl.write(wiki_summary(url))
        time_taken()
    elif val == "Images":
        sl.write("## Wikipedia Images:")
        sl.write("##")
        img_list = wiki_images(url)
        img_len = len(img_list)
        for i in range(0, img_len):
            sl.image(
                img_list[i],
                caption=img_list[i].split("/")[-1].split(".")[0],
                width=200,
                use_column_width="always",
            )
            sl.markdown("""-----""")
        time_taken()
    elif val == "Refrences":
        sl.write("## Wikipedia refrences:")
        sl.write("##")
        for i, refs in enumerate(wiki_refrences(url), 1):
            sl.write(i, " - ", refs)
        time_taken()
    elif val == "Top 10 Most Frequent Words":
        sl.write("## Word Frequency Analysis:")
        sl.write("##")
        text = wk.page(url).content
        top10 = freq_words(text)
        words, counts = zip(*top10)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(words, counts, color="skyblue")
        for bar, count in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                str(count),
                ha="center",
                va="bottom",
            )
        ax.set_title("Top 10 Most Frequent Words")
        ax.set_xlabel("Words")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        sl.pyplot(fig)
        sl.markdown("""-----""")
        time_taken()
    elif val == "Sentimental Analysis":
        sl.write("## Sentimental Analysis:")
        sl.write("##")
        sentiment_results = wiki_sentimental_analysis(url)
        sentiment_label = sentiment_results["sentiment_label"]
        sentiment_score = round(sentiment_results["sentiment_polarity"], 3)
        sentiment_df = pd.DataFrame(sentiment_results["sentiment_words"])
        sl.write(f"**Sentiment status:** {sentiment_label}")
        sl.write(f"**Sentiment value:** {sentiment_score}")
        sl.write("##")
        if sentiment_label == "Positive":
            sl.image(
                "sentimental_images\happy_face.png",
                width=200,
            )
        elif sentiment_label == "Negative":
            sl.image(
                "sentimental_images\sad_face.png",
                width=100,
            )
        else:
            sl.image(
                "sentimental_images\ordinary_face.png",
                width=100,
            )
        sl.write("##")
        sl.write(f"### Sentiment {sentiment_label} Words:")
        sl.write("##")
        sl.write(sentiment_df)
        time_taken()
    else:
        sl.write("## Wikipedia Text:")
        sl.write("##")
        sl.write(wiki_content(url))
        sl.write("##")
        sl.write("## Wikipedia Summary:")
        sl.write("##")
        sl.write(wiki_summary(url))
        sl.write("##")
        sl.write("## Wikipedia Images:")
        sl.write("##")
        img_list = wiki_images(url)
        img_len = len(img_list)
        for i in range(0, img_len):
            sl.image(
                img_list[i],
                caption=img_list[i].split("/")[-1].split(".")[0],
                width=200,
                use_column_width="always",
            )
        sl.write("##")
        sl.write("## Wikipedia refrences:")
        sl.write("##")
        for i, refs in enumerate(wiki_refrences(url), 1):
            sl.write(i, " - ", refs)
        sl.write("##")
        sl.write("## Word Frequency Analysis:")
        sl.write("##")
        text = wk.page(url).content
        top10 = freq_words(text)
        words, counts = zip(*top10)
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(words, counts, color="skyblue")
        for bar, count in zip(bars, counts):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height(),
                str(count),
                ha="center",
                va="bottom",
            )
        ax.set_title("Top 10 Most Frequent Words")
        ax.set_xlabel("Words")
        ax.set_ylabel("Count")
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        sl.pyplot(fig)
        sl.markdown("""-----""")
        sl.write("##")
        sl.write("## Sentimental Analysis:")
        sl.write("##")
        sentiment_results = wiki_sentimental_analysis(url)
        sentiment_label = sentiment_results["sentiment_label"]
        sentiment_score = round(sentiment_results["sentiment_polarity"], 3)
        sentiment_df = pd.DataFrame(sentiment_results["sentiment_words"])
        sl.write(f"**Sentiment status:** {sentiment_label}")
        sl.write(f"**Sentiment value:** {sentiment_score}")
        sl.write("##")
        if sentiment_label == "Positive":
            sl.image(
                "sentimental_images\happy_face.png",
                width=200,
            )
        elif sentiment_label == "Negative":
            sl.image(
                "sentimental_images\sad_face.png",
                width=100,
            )
        else:
            sl.image(
                "sentimental_images\ordinary_face.png",
                width=100,
            )
        sl.write("##")
        sl.write(f"### Sentiment {sentiment_label} Words:")
        sl.write("##")
        sl.write(sentiment_df)
        time_taken()
