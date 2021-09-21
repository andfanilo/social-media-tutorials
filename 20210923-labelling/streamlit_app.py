import requests
import streamlit as st

if "counter" not in st.session_state:
    st.session_state["counter"] = 0

N_IMAGES = 10

def on_submit(label, img):
    with open(f"images/{label}.png", "wb") as f:
        f.write(img)
    st.session_state["counter"] += 1

@st.cache
def download_random_image(i: int):
    return requests.get(
        "https://source.unsplash.com/random/600x400"
        ).content

if st.session_state["counter"] == N_IMAGES:
    st.info("DONE")
    st.stop()

img = download_random_image(st.session_state["counter"])

st.image(img)
label = st.text_input("Label")
st.button("Submit", on_click=on_submit, args=(label, img))
