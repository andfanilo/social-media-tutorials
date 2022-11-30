import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from utils import init

st.title("Switch Pages???")

if st.button("Switch page"):
    switch_page("Vertical Space")