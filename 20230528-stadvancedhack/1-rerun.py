import time
from datetime import datetime

import numpy as np
import streamlit as st
from streamlit.runtime.scriptrunner import add_script_run_ctx

start = time.time()

if "produced_images" not in st.session_state:
    st.session_state.produced_images = 0

def produce_image():
    SIZE_IMAGE = 512
    image = np.random.random((SIZE_IMAGE, SIZE_IMAGE)).astype(np.float32)
    n = st.session_state.produced_images % SIZE_IMAGE
    m = st.session_state.produced_images % SIZE_IMAGE
    image[n : n + 10] = 0
    image[:, m : m + 10] = 1
    st.session_state.produced_images += 1
    return image


produce_delay = 1 / st.slider(
    "Produce images Frequency (img / second)", 1, 100, 2
)

st.image(
    produce_image(),
    caption=f"Consumed images: {st.session_state.produced_images}, {str(datetime.now())}"
)

time.sleep(produce_delay)

end = time.time()
st.write(1 / (end - start))

st.experimental_rerun()