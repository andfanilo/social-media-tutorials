import streamlit as st

from streamlit_extras.badges import badge
from streamlit_extras.mention import mention
from streamlit_extras.keyboard_text import key
from streamlit_extras.keyboard_text import load_key_css
from markdownlit import mdlit

from utils import init

init()

st.title("Custom link displays")

c1, c2, c3, c4 = st.columns(4)

with c1:
    badge(type="pypi", name="streamlit-drawable-canvas")
    badge(type="github", name="andfanilo/streamlit-echarts")
    badge(type="streamlit", url="https://lottie.streamlit.app/")
    badge(type="twitter", name="andfanilo")

with c2:
    mention(
        label="My ECharts Demo!",
        icon="streamlit",
        url="https://echarts.streamlitapp.com",
    )
    mention(
        label="ECharts Source Code",
        icon="github",
        url="https://github.com/andfanilo/streamlit-echarts",
    )
    mention(
        label="Follow me on Twitter",
        icon="twitter",
        url="https://twitter.com/andfanilo",
    )

with c3:
    load_key_css()
    st.write(
        f"To check the Developer Tools: {key('CTRL+Maj+I', write=False)}",
        unsafe_allow_html=True,
    )

with c4:
    mdlit(
        """You can find a Lottie demo on @(https://lottie.streamlit.app). 
        Or you can @(✨)(use this instead)(https://extras.streamlit.app).
        You can color text easily too: [red]beautiful[/red] [blue]set[/blue] [orange]of[/orange]
        [violet]colors[/violet].
        """
    )