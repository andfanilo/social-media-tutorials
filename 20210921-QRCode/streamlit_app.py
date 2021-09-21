import io
import qrcode
import streamlit as st


st.title("QRCode Generator")
st.caption("Like & follow for more!")


url = st.text_input(
    "URL to encode:", 
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
)


img = qrcode.make(url)
virtualfile = io.BytesIO()
img.save(virtualfile)


st.image(virtualfile)