import streamlit as st
import streamlit.components.v1 as components

st.title("CSS Hack tests")

# Components Bootstrap
st.subheader("Integrate Bootstrap")
components.html(
    """
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css">
<script src="https://code.jquery.com/jquery-3.2.1.slim.min.js"></script>
<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js"></script>
<div class="card" style="width: 18rem;">
  <img class="card-img-top" src="https://cataas.com/cat?height=200" alt="Card image cap">
  <div class="card-body">
    <h5 class="card-title">A Bootstrap Card</h5>
    <p class="card-text">In Streamlit!</p>
    <a href="https://cataas.com/" class="btn btn-primary">Go to cat API</a>
  </div>
</div>
""",
    height=400,
)

# STYLE WITH CSS THROUGH MARKDOWN
if st.checkbox("Make all buttons round", False):
    st.markdown(
        """
    <style>
    .stButton>button {
        border-radius: 50%;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )

# STYLE WITH JS THROUGH HTML IFRAME
st.subheader("Style particular buttons")

st.button("Hello Red")
st.button("Hello Blue")
st.button("Hello Green")

components.html(
    """
<script>
const elements = window.parent.document.querySelectorAll('.stButton button')
elements[0].style.backgroundColor = 'lightcoral'
elements[1].style.backgroundColor = 'lightblue'
elements[2].style.backgroundColor = 'lightgreen'
</script>
""",
    height=0,
    width=0,
)
