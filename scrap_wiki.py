import requests
import nltk
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
import re

url = input("Enter the Wiki url: ")

res = requests.get(url)

wiki_text = BeautifulSoup(res.text, "html.parser")

text = ""
for para in wiki_text.select("p"):
    text += para.getText()


text = re.sub(r"\[[0-9]*\]", " ", text)
text = re.sub(r"\s+", " ", text)
text = text.lower()
text = re.sub(r"\d", " ", text)
text = re.sub(r"\s+", " ", text)

sentences = nltk.sent_tokenize(text)

sentences = [nltk.word_tokenize(sentence) for sentence in sentences]

print(sentences)
