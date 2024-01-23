import requests
from bs4 import BeautifulSoup
import re


def text_scrap(url):
    res = requests.get(url)

    wiki_text = BeautifulSoup(res.text, "html.parser")

    text = ""
    for para in wiki_text.select("p"):
        text += para.getText() + "\n"

    text = re.sub(r"\[[0-9]*\]", " ", text)
    text = re.sub(r"\s+", " ", text)
    text = text.lower()
    text = re.sub(r"\[citation needed\]", " ", text)
    text = re.sub(r"`", "", text)
    text = text.replace("[", "(")
    text = text.replace("]", ")")
    return text
