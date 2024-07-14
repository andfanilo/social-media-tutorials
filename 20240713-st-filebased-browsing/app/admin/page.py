import streamlit as st

st.title("Admin Panel")

with st.form("login_form"):
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    submitted = st.form_submit_button("Login", type="primary")

if submitted:
    if username == "admin" and password == "password":
        st.success("Login successful!")
    else:
        st.error("Incorrect username or password")