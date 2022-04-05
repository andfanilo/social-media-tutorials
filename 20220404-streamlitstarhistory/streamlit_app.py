"""
pip install ghapi pandas plotly streamlit 
streamlit run streamlit_app.py
"""
import pandas as pd
import plotly.express as px
import streamlit as st
from fastcore.net import HTTP404NotFoundError
from ghapi.all import GhApi
from ghapi.all import pages

st.title("Streamlit Star History")
st.sidebar.header("Configuration")


@st.experimental_singleton
def load_api():
    token = st.secrets["github"]["key"]
    return GhApi(token=token)


st.checkbox("Create Github API Connection")
st.checkbox("Check rate-limit")
st.checkbox("Add text input for user")
st.checkbox("Check each repo existence")
st.checkbox("Download star data from API")
st.checkbox("Display plot with Plotly")


@st.experimental_memo
def check_repo(repo: str):
    try:
        username, repository = repo.split("/")
        load_api().activity.list_stargazers_for_repo(username, repository)
        return True
    except ValueError:
        return False
    except HTTP404NotFoundError:
        return False


def check_rate_limit():
    return load_api().rate_limit.get()


@st.experimental_memo
def search_stargazers(repo, per_page=30):
    api = load_api()
    username, repository = repo.split("/")

    api.activity.list_stargazers_for_repo(username, repository, per_page=per_page)
    n_pages = api.last_page()

    all_pages = pages(
        api.activity.list_stargazers_for_repo,
        n_pages,
        username,
        repository,
        per_page=per_page,
        headers={"Accept": "application/vnd.github.v3.star+json"},
    )

    data = [
        {"date": item["starred_at"], "count": 1} for page in all_pages for item in page
    ]
    df = pd.DataFrame(data)
    df["date"] = pd.to_datetime(df["date"])
    df = df.resample("W-Mon", on="date").sum().cumsum()
    df["repo"] = repo
    return df


all_repos = st.sidebar.text_area("Enter repo as user/repo")
st.sidebar.write(check_rate_limit())

if all_repos == "":
    st.warning("Add repo info")
    st.stop()

for repo in all_repos.rstrip().splitlines():
    if not check_repo(repo):
        st.warning(f"Repo {repo} does not exist")
        st.stop()

list_dfs = [search_stargazers(repo) for repo in all_repos.rstrip().splitlines()]
df = pd.concat(list_dfs)

with st.expander("Check final dataframe"):
    st.dataframe(df)

fig = px.line(df, x=df.index, y="count", color="repo")
fig.update_layout(hovermode="x")
st.plotly_chart(fig)
