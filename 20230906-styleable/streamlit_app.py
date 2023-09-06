import streamlit as st
import plotly.express as px
from streamlit_extras.stylable_container import stylable_container

st.title("Hello :balloon:")

c1, c2 = st.columns(2)
with c1:
    with stylable_container(
        key="cat_container",
        css_styles=[
            """
        {
            background-color: coral;
            padding: 0.5em;
            border-radius: 1em;
        }
        """,
            """
        .stMarkdown {
            padding-right: 1.5em;
        }
        """,
        ],
    ):
        st.markdown(
            "The cat (Felis catus) is a domestic species of small carnivorous mammal. It is the only domesticated species in the family Felidae and is commonly referred to as the domestic cat or house cat to distinguish it from the wild members of the family. Cats are commonly kept as house pets but can also be farm cats or feral cats; the feral cat ranges freely and avoids human contact."
        )

with c2:
    with stylable_container(
        key="cat_image",
        css_styles="""
        img {
            border-radius: 2em;
        }
        """,
    ):
        st.image("./cat.jpg")

st.divider()

c1, c2, _ = st.columns([1, 1, 2])

with c1:
    with stylable_container(
        key="green_button",
        css_styles="""
            button {
                background-color: green;
                color: white;
                border-radius: 20px;
            }
            """,
    ):
        st.button("Green button")

with c2:
    with stylable_container(
        key="black_button",
        css_styles=[
            """
            button {
                border: solid .3em #292746;
                border-radius: 20px;
                color: #fff;
                background-color: #292746;
            }
            """,
            """
            button:hover {
                background-color: red;
            }
            """,
        ],
    ):
        st.button("Hover in Red")

with stylable_container(
    key="st_selectbox",
    css_styles=[
        """
        div[data-baseweb="select"] > div {
            background-color: red;
        }
        """,
        """
        div[role="listbox"] ul {
            background-color: green;
        }
        """,
    ],
):
    st.selectbox("Hello", ("Streamlit", "is", "fun"))


with stylable_container(
    key="container_with_border",
    css_styles=[
        """
        {
            background-color: green;
            border: 8px double rgba(49, 51, 63, 0.2);
            border-radius: 0.5rem;
            padding: 1em;
        }
        """,
        """
        .stDataFrame {

        }
        """,
    ],
):
    st.markdown("This is a container with a border.")
    df = px.data.gapminder().query("country=='Canada'")
    st.dataframe(df, use_container_width=True)
    st.plotly_chart(
        px.line(df, x="year", y="lifeExp", title="Life expectancy in Canada"),
        use_container_width=True,
    )
