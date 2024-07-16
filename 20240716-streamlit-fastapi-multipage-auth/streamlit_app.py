import jwt
import requests
import streamlit as st

st.set_page_config(
    page_title="My Dashboard", page_icon=":material/dashboard:", layout="wide"
)

BASE_URL = "http://localhost:8000"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"

if "current_user" not in st.session_state:
    st.session_state.current_user = ""
if "jwt_token" not in st.session_state:
    st.session_state.jwt_token = ""


def get_jwt_token(username):
    """Fetches a JWT token from the FastAPI server."""
    url = f"{BASE_URL}/token/{username}"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        print(f"Error fetching token: {response.status_code}")
        return None


@st.experimental_dialog("Authenticate without a password")
def authenticate_with_user():
    users = ["Fanilo", "Jenny", "John", "Kkura 🌸"]
    username = st.selectbox("Choose a user to auth with", options=users, index=None)

    if st.button("Authenticate", type="primary", disabled=not username):
        with st.spinner(f"Authenticating {username}, please wait for FastAPI to respond..."):
            token = get_jwt_token(username)

        st.session_state.current_user = username
        st.session_state.jwt_token = token

        st.rerun()


if not (st.session_state.current_user and st.session_state.jwt_token):
    authenticate_with_user()
    st.stop()


st.title("My Dashboard")

navigation_tree = {
    "Main": [
        st.Page("app/home.py", title="Home", icon=":material/home:"),
        st.Page("app/about.py", title="About", icon=":material/person:"),
    ],
}


user_claims = jwt.decode(
    jwt=st.session_state.jwt_token,
    key=SECRET_KEY,
    algorithms=ALGORITHM,
)

with st.sidebar:
    st.header("Debug")
    st.markdown("Decoded JWT:")
    st.json(user_claims)
    st.markdown(f"JWT: :violet[{st.session_state.jwt_token}]")

if "viewer" in user_claims.get("roles", []):
    navigation_tree.update(
        {
            "Reports": [
                st.Page(
                    "app/mom.py",
                    title="Month Over Month",
                    icon=":material/attach_money:",
                ),
                st.Page(
                    "app/quarterly.py",
                    title="Quarterly",
                    icon=":material/clock_loader_80:",
                ),
            ],
        }
    )
if "admin" in user_claims.get("roles", []):
    navigation_tree.update(
        {
            "Configuration": [
                st.Page(
                    "app/settings.py",
                    title="Settings",
                    icon=":material/settings:",
                )
            ]
        }
    )

nav = st.navigation(navigation_tree, position="sidebar")
nav.run()

if st.button("Logout"):
    st.session_state.current_user = ""
    st.session_state.jwt_token = ""
    st.rerun()