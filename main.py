# for the streamlit

import streamlit as st
from scrap_wiki import text_scrap


url = st.text_input("Enter the Wikipedia page URL")

submit_btn = st.button("Enter")

if submit_btn:
    text = text_scrap(url)
    st.write(text)
