import streamlit as sl
import wikipedia as wk


with sl.form("Wiki Search"):
    url = sl.text_input("Enter the Wikipedia page URL")
    url = url.split("/")[-1]
    val = sl.selectbox(
        "Search for", options=["Content", "Summary", "Images", "Refrences", "All data"]
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


if submit_btn:
    if val == "Content":
        sl.write("## Wikipedia Text:")
        sl.write("##")
        sl.write(wiki_content(url))
    elif val == "Summary":
        sl.write("## Wikipedia Summary:")
        sl.write("##")
        sl.write(wiki_summary(url))
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
    elif val == "Refrences":
        sl.write("## Wikipedia refrences:")
        sl.write("##")
        for i, refs in enumerate(wiki_refrences(url), 1):
            sl.write(i, " - ", refs)
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
