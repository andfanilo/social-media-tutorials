import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Complaining Dashboard",
    page_icon="📞",
    layout="wide",
)
st.logo("./img/round_fan.png")

if "options" not in st.session_state:
    st.session_state.options = None

complaints_page = st.Page(
    "./app/complaints.py",
    title="Complaints Dashboard", 
    icon=":material/sentiment_extremely_dissatisfied:",
)
about_page = st.Page(
    "./app/about.py", 
    title="About the Data", 
    icon=":material/home:",
)
selected_page = st.navigation([complaints_page, about_page])
selected_page.run()
