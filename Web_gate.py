import streamlit as st
from test import mark
st.write("## GATE SCORE CHECKER")
url=st.text_input("Enter Gate paper url")
button = st.button("Calculate")
if button:
    marks= mark(url)
    st.write(f"SCORE {marks}")