import streamlit as st

from annotated_text import annotated_text, annotation
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.word_importances import format_word_importances

from utils import init

init()

st.title("Annotating some text")
annotated_text(
    "This ",
    ("is", "verb", "#8ef"),
    " some ",
    ("annotated", "adj", "#faa"),
    ("text", "noun", "#afa"),
    " for those of ",
    ("you", "pronoun", "#fea"),
    " who ",
    annotation("like", "verb", color="#1E1E1E", border="1px dashed red"),
    " this sort of ",
    ("thing", "noun", "#afa"),
)

text = "Streamlit Extras is a library to help you discover, learn, share and use Streamlit bits of code!"
html = format_word_importances(
    words=text.split(),
    importances=(0.1, 0.2, 0, -1, 0.1, 0, 0, 0.2, 0.3, 0.8, 0.9, 0.6, 0.3, 0.1, 0, 0, 0),  # fmt: skip
)
add_vertical_space(2)
st.write(html, unsafe_allow_html=True)