import streamlit as sl
import wikipedia as wk


with sl.form("Wiki Search"):
    url = sl.text_input("Enter the Wikipedia page URL")
    url = url.split("/")[-1]
    text, summary, images, refrences = sl.columns(4)
    text_submit_btn = text.form_submit_button("Content")
    summary_submit_btn = summary.form_submit_button("Summary")
    images_submit_btn = images.form_submit_button("Images")
    refrences_submit_btn = refrences.form_submit_button("Refrences")

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


if text_submit_btn:
    sl.write("## Wikipedia Text:")
    sl.write("##")
    sl.write(wiki_content(url))

if summary_submit_btn:
    sl.write("## Wikipedia Summary:")
    sl.write("##")
    sl.write(wiki_summary(url))

if images_submit_btn:
    sl.write("## Wikipedia Summary:")
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

if refrences_submit_btn:
    sl.write("## Wikipedia refrences:")
    sl.write("##")
    for i, refs in enumerate(wiki_refrences(url), 1):
        sl.write(i, " - ", refs)
