import streamlit as st
import json
from streamlit_extras.function_explorer import function_explorer

from utils import init

init()

st.title("Explore a function")

output = function_explorer(json.loads)
st.json(output)