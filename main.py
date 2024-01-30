import streamlit as sl
import wikipedia as wk
from time import time
from collections import Counter
import matplotlib.pyplot as plt
from textblob import TextBlob
import pandas as pd


def show_warning(message):
    sl.warning(message)

sl.set_page_config(
    page_title="Wiki Scraper",
    page_icon="🧱"
)

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
    try:
        text = wk.page(url).content
        text = text.replace("`", "")
        return text
    except Exception as e:
        show_warning(f"Error retrieving content: {str(e)}")
        return None


def wiki_summary(url):
    try:
        summ = wk.summary(url, sentences=10)
        summ = summ.replace("`", "")
        return summ
    except Exception as e:
        show_warning(f"Error retrieving summary: {str(e)}")
        return None


def wiki_images(url):
    try:
        imgs = wk.page(url)
        img_urls = imgs.images
        return img_urls
    except Exception as e:
        show_warning(f"Error retrieving images: {str(e)}")
        return None


def wiki_refrences(url):
    try:
        refs = wk.page(url)
        ref_urls = refs.references
        return ref_urls
    except Exception as e:
        show_warning(f"Error retrieving references: {str(e)}")
        return None


def freq_words(text):
    try:
        words = text.split()
        word_counts = Counter(words)
        top10 = word_counts.most_common(10)
        top10 = sorted(top10, key=lambda x: x[0].lower())
        return top10
    except Exception as e:
        show_warning(f"Error performing word frequency analysis: {str(e)}")
        return None


def wiki_sentimental_analysis(url):
    try:
        text = wk.page(url).content
        blob = TextBlob(text)
        sentiment_polarity = blob.sentiment.polarity

        if sentiment_polarity > 0:
            sentiment_label = "Positive"
            sentiment_words = [
                {
                    "word": word.lower(),
                    "score": blob.sentiment.polarity,
                    "frequency": count,
                }
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
                {
                    "word": word.lower(),
                    "score": blob.sentiment.polarity,
                    "frequency": count,
                }
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
                {
                    "word": word.lower(),
                    "score": blob.sentiment.polarity,
                    "frequency": count,
                }
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
    except Exception as e:
        show_warning(f"Error performing sentimental analysis: {str(e)}")
        return None


def time_taken():
    end = time()
    time_taken = format((end - start), ".2f")
    time_taken = "Searched in " + str(time_taken) + " seconds"
    sl.success(time_taken)


if submit_btn:
    start = time()
    try:
        if val == "Content":
            sl.write("## Wikipedia Text:")
            sl.write("##")
            content = wiki_content(url)
            if content is not None:
                sl.write(content)
            time_taken()
        elif val == "Summary":
            sl.write("## Wikipedia Summary:")
            sl.write("##")
            summary = wiki_summary(url)
            if summary is not None:
                sl.write(summary)
            time_taken()
        elif val == "Images":
            sl.write("## Wikipedia Images:")
            sl.write("##")
            img_list = wiki_images(url)
            if img_list is not None:
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
            references = wiki_refrences(url)
            if references is not None:
                for i, refs in enumerate(references, 1):
                    sl.write(i, " - ", refs)
            time_taken()
        elif val == "Top 10 Most Frequent Words":
            sl.write("## Word Frequency Analysis:")
            sl.write("##")
            text = wk.page(url).content
            top10 = freq_words(text)
            if top10 is not None:
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
            if sentiment_results is not None:
                sentiment_label = sentiment_results["sentiment_label"]
                sentiment_score = round(sentiment_results["sentiment_polarity"], 3)
                sentiment_df = pd.DataFrame(sentiment_results["sentiment_words"])
                sl.write(f"**Sentiment status:** {sentiment_label}")
                sl.write(f"**Sentiment value:** {sentiment_score}")
                sl.write("##")
                if sentiment_label == "Positive":
                    sl.image(
                        "happy_face.png",
                        width=200,
                    )
                elif sentiment_label == "Negative":
                    sl.image(
                        "sad_face.png",
                        width=100,
                    )
                else:
                    sl.image(
                        "ordinary_face.png",
                        width=100,
                    )
                sl.write("##")
                sl.write(f"### Sentiment {sentiment_label} Words:")
                sl.write("##")
                sl.write(sentiment_df)
                sl.write("##")
                sl.write("### Word Frequency Chart:")
                fig, ax = plt.subplots()
                bars = ax.bar(
                    sentiment_df["word"], sentiment_df["frequency"], color="skyblue"
                )
                for bar, count in zip(bars, sentiment_df["frequency"]):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height(),
                        str(count),
                        ha="center",
                        va="bottom",
                    )
                ax.set_xlabel("Words")
                ax.set_ylabel("Frequency")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                sl.pyplot(fig)
                time_taken()
        else:
            sl.write("## Wikipedia Text:")
            sl.write("##")
            content = wiki_content(url)
            if content is not None:
                sl.write(content)
            sl.write("##")
            sl.write("## Wikipedia Summary:")
            sl.write("##")
            summary = wiki_summary(url)
            if summary is not None:
                sl.write(summary)
            sl.write("##")
            sl.write("## Wikipedia Images:")
            sl.write("##")
            img_list = wiki_images(url)
            if img_list is not None:
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
            references = wiki_refrences(url)
            if references is not None:
                for i, refs in enumerate(references, 1):
                    sl.write(i, " - ", refs)
            sl.write("##")
            sl.write("## Word Frequency Analysis:")
            sl.write("##")
            text = wk.page(url).content
            top10 = freq_words(text)
            if top10 is not None:
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
            if sentiment_results is not None:
                sentiment_label = sentiment_results["sentiment_label"]
                sentiment_score = round(sentiment_results["sentiment_polarity"], 3)
                sentiment_df = pd.DataFrame(sentiment_results["sentiment_words"])
                sl.write(f"**Sentiment status:** {sentiment_label}")
                sl.write(f"**Sentiment value:** {sentiment_score}")
                sl.write("##")
                if sentiment_label == "Positive":
                    sl.image(
                        "happy_face.png",
                        width=200,
                    )
                elif sentiment_label == "Negative":
                    sl.image(
                        "sad_face.png",
                        width=100,
                    )
                else:
                    sl.image(
                        "ordinary_face.png",
                        width=100,
                    )
                sl.write("##")
                sl.write(f"### Sentiment {sentiment_label} Words:")
                sl.write("##")
                sl.write(sentiment_df)
                sl.write("##")
                sl.write("### Sentiment words frequency chart:")
                fig, ax = plt.subplots()
                bars = ax.bar(
                    sentiment_df["word"], sentiment_df["frequency"], color="skyblue"
                )
                for bar, count in zip(bars, sentiment_df["frequency"]):
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,
                        bar.get_height(),
                        str(count),
                        ha="center",
                        va="bottom",
                    )
                ax.set_xlabel("Words")
                ax.set_ylabel("Frequency")
                plt.xticks(rotation=45, ha="right")
                plt.tight_layout()
                sl.pyplot(fig)
                time_taken()
    except Exception as e:
        show_warning(f"An unexpected error occurred: {str(e)}")
