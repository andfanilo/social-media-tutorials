import streamlit as st
from streamlit_faker import get_streamlit_faker

from utils import init

init()

st.title("App Logo In The Sidebar")

fake = get_streamlit_faker(seed=42)
fake.markdown()
fake.altair_chart()