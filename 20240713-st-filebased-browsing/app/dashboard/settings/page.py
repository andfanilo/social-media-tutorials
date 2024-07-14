import streamlit as st

st.title("Settings")

with st.form("settings_form"):
    st.text_input("Username", value="admin")
    st.text_input("Password", type="password", value="password")
    st.text_input("Email", value="admin@example.com")
    st.text_area("About", value="This is a sample about section.")
    st.text_input("Website", value="https://www.example.com")
    st.text_input("Social Media Links", value="https://www.facebook.com")
    st.text_input("Contact Information", value="123-456-7890")
    st.text_input("Address", value="123 Main Street, Anytown, USA")
    st.text_input("Copyright", value="Copyright © 2023")
    st.form_submit_button("Save Changes", type="primary")