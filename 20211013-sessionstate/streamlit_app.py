import streamlit as st

st.title("Hello Streamlit")

# Slide 2 - Nested button

first_click = st.button("Click me")

if first_click:
    second_click = st.button("BALLOOONS!")
    if second_click:
        st.balloons()

# Slide 3 - Session State

if "counter" not in st.session_state:
    st.session_state.counter = 0

st.write(st.session_state.counter)
st.session_state.counter += 1

if st.session_state.counter < 10:
    st.experimental_rerun()

# Slide 4 - Session State manipulation

if "key" not in st.session_state:
    st.session_state["key"] = "value"

st.write(st.session_state.key)

st.session_state.key = "value2"
st.session_state["key"] = "value2"

del st.session_state["key"]

# Slide 5 - Widget keys

st.text_input("Your name", key="name")
st.write(st.session_state.name)

# Slide 6 - Callbacks

if "balloons" not in st.session_state:
    st.session_state.balloons = 0


def send_balloons(increment_value):
    st.balloons()
    st.session_state.balloons += increment_value


st.button("BALLOOONS!", on_click=send_balloons, args=(1,))
st.markdown(f"You launched {st.session_state.balloons} balloons")

# Slide 7 - Nested button + state

if "first_click" not in st.session_state:
    st.session_state.first_click = False

if st.button("Click me") or st.session_state.first_click:
    st.session_state.first_click = True
    if st.button("BALLOOONS!"):
        st.balloons()
