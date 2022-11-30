import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from utils import init

init()

st.title("Add some space")
add_n_lines = st.slider("Add n vertical lines below this", 1, 20, 5)
add_vertical_space(add_n_lines)
st.markdown("Hello dear viewer!")