import time
import streamlit as st
import streamlit.components.v1 as components


def read_js():
    with open("index.js") as f:
        return f.read()


if "counter" not in st.session_state:
    st.session_state.counter = 0


def left_callback():
    st.session_state.counter -= 1


def right_callback():
    st.session_state.counter += 1


def copy_callback(placeholder):
    copy_text = f'"Value to clipboard is {st.session_state.counter}"'
    with placeholder:
        components.html(
            f"""
    <script>
    console.log({copy_text});
    //window.parent.navigator.clipboard.readText().then((d) => {{console.log(d)}})
    window.parent.navigator.clipboard.writeText({copy_text})
    </script>
        """,
            height=0,
            width=0,
        )
        time.sleep(1)


st.title("Hacking Streamlit Frontend")
st.caption("Press left / right arrow keys to simulate decrement / increment button click")
st.caption("Press Enter key to simulate Copy to clipboard button click")
left_col, right_col, copy_button, _ = st.columns([1, 1, 2, 3])

left_col.button("Decrement", on_click=left_callback)
right_col.button("Increment", on_click=right_callback)

st.metric("Counter", st.session_state.counter)

iframe_copy_placeholder = st.empty()
copy_button.button(
    "Copy To Clipboard", on_click=copy_callback, args=(iframe_copy_placeholder,)
)

components.html(
    f"<script>{read_js()}</script>",
    height=0,
    width=0,
)
