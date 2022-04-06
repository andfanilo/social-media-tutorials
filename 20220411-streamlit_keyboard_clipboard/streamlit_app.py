import streamlit as st
import streamlit.components.v1 as components


def read_index_html(copy_text: int):
    with open("index.html") as f:
        return f.read().replace("python_string", f'"Counter value is {copy_text}"')


if "counter" not in st.session_state:
    st.session_state.counter = 0


def left_callback():
    st.session_state.counter -= 1


def right_callback():
    st.session_state.counter += 1


st.title("Hacking Streamlit Frontend")
st.caption(
    "Press left / right arrow keys to simulate decrement / increment button click"
)
st.caption("Press Enter key to simulate Copy to clipboard button click")
left_col, right_col, _ = st.columns([1, 1, 3])

left_col.button("Decrement", on_click=left_callback)
right_col.button("Increment", on_click=right_callback)

st.metric("Counter", st.session_state.counter)

components.html(
    read_index_html(st.session_state.counter),
    height=0,
    width=0,
)
