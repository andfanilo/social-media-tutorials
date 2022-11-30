import streamlit as st

from streamlit_extras.metric_cards import style_metric_cards
from streamlit_card import card

from utils import init

init()

st.title("My Youtube Dashboard")
c1, c2, c3 = st.columns(3)
c1.metric(label="Views", value=12400, delta=4400)
c2.metric(label="Watch Time", value=747.3, delta=-214)
c3.metric(label="Subscribers", value=193, delta=0)
style_metric_cards(border_left_color="red")


card(
    title="Youtube Dashboard",
    text="Jump to full analytics report",
    image="http://placekitten.com/300/250",
    url="https://studio.youtube.com",
)