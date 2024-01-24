import streamlit as sl
import wikipedia as wk


with sl.form("Wiki Search"):
    url = sl.text_input("Enter the Wikipedia page URL")
    url = url.split("/")[-1]
    
    submit_btn = sl.form_submit_button("Search")


sl.write("## Wikipedia Content")

def wiki_content(url):
    text = wk.page(url).content
    text = text.replace("`", "")
    return text

def wiki_summary(url):
    text = wk.page(url).summary
    text = text.replace("`", "")
    return text

if submit_btn:
    sl.write(wiki_content(url))

summary_btn = sl.button("Find Summary")
if summary_btn:
    sl.write("## Summary")
    sl.write(wiki_summary(url))
