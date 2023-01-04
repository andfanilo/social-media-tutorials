import streamlit as st

st.title("My Goals for 2023 :tada:")
st.image(
    "https://images.unsplash.com/photo-1585776245865-b92df54c6b25?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=800"
)

all_goals = [
    ("Eat Healthy", False),
    ("Subscribe", True),
    ("Learn CSS", False),
]

for goal, status in all_goals:
    st.markdown(f"* [{'x' if status else ' '}] {goal}")
