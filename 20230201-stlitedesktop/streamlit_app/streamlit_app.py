import base64
import pathlib
from PIL import Image

import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Winter app",
    page_icon=":penguin:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

folder = pathlib.Path(__file__).parent 
iris_df = px.data.iris()

@st.experimental_memo
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

img = get_img_as_base64("img/tree.png")

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://images.unsplash.com/photo-1477601263568-180e2c6d046e");
background-size: 200%;
background-position: 30% 45%;
background-repeat: no-repeat;
background-attachment: local;
}}

[data-testid="stSidebar"] > div:first-child {{
background-image: url("data:image/png;base64,{img}");
background-position: 50% 45%;
background-size: 400%;
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

st.title("It's winter!")
st.markdown(
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
)
c1, c2, c3 = st.columns(3)
c1.dataframe(iris_df, height=600, use_container_width=True)
c2.plotly_chart(
    px.scatter(
        iris_df, 
        x="sepal_width", 
        y="sepal_length", 
        color="species",
        height=600,
    ),
    use_container_width=True,
)
c3.image(
    Image.open("img/penguin.jpg"), 
    use_column_width="always"
)