import base64
import json

import streamlit as st
from streamlit_lottie import st_lottie

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

@st.experimental_memo
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)

img = get_img_as_base64("img/tree.png")
snow_animation = load_lottiefile("img/lottie-snow.json")

page_bg_img = f"""
<style>
[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
}}

[data-testid="stSidebarNav"] span {{
color:white;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

[data-testid="stToolbar"] {{
right: 2rem;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

st_lottie(snow_animation, height=600, key="initial")