import streamlit as st
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

iris = datasets.load_iris()
X = iris.data
y = iris.target

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42
)

st.title("Forms")

# Slide 1

n_estimators = st.slider("Num estimators", 1, 20)
max_depth = st.slider("Max depth", 1, 20)
clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
clf.fit(X_train, y_train)

# Slide 2

with st.form(key="my_form"):
    n_estimators = st.slider("Num estimators", 1, 20)
    max_depth = st.slider("Max depth", 1, 20)
    submit_button_click = st.form_submit_button(label="Rerun")

if submit_button_click:
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    clf.fit(X_train, y_train)

# Slide 2

if "counter" not in st.session_state:
    st.session_state.counter = 0

def _send_data():
    st.session_state.counter += 1

form = st.form(key="my_form")
n_estimators = form.slider("Num estimators", 1, 20)
max_depth = form.slider("Max depth", 1, 20)
submit_button_click = st.form_submit_button(
    label="Rerun",
    on_click=_send_data
)

if submit_button_click:
    clf = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth)
    clf.fit(X_train, y_train)

st.write(f"Your model was trained **{st.session_state.counter}** times :scream:")