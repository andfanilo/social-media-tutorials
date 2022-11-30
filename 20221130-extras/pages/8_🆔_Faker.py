import streamlit as st
from streamlit_faker import get_streamlit_faker

from utils import init

init()

st.title("Quick Prototype")

seed = st.number_input("Seed", 0, 100, 42)
st.markdown("---")
fake = get_streamlit_faker(seed=seed)
fake.markdown()
fake.info(icon="💡")
fake.selectbox()
fake.slider()
fake.metric()
fake.altair_chart()
fake.pyplot()