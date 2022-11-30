import streamlit as st
from streamlit_extras.buy_me_a_coffee import button

from utils import init

init()

st.title("Thanks for watching!")
button(username="andfanilo", floating=False, width=221)
