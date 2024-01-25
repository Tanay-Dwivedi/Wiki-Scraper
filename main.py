import streamlit as sl
import wikipedia as wk
from time import time
from collections import Counter
import matplotlib.pyplot as plt

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
        time_taken()
