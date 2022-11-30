import streamlit as st

from streamlit_extras.colored_header import colored_header
from st_keyup import st_keyup

from utils import init

init()

colored_header(
    label="A reactive-like text input",
    description="Demo below",
    color_name="violet-70",
)

st.write("## Classical Input")
out = st.text_input("What is your name?")
st.write(f"Hello {out}")
st.write("## Reactive-like Input")
out2 = st_keyup("What is your name again?")
st.write(f"Hello {out2}")
