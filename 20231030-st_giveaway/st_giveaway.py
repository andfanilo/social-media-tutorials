"""Run with streamlit run st_giveaway.py from root of project"""
import os
import pickle
from pathlib import Path

import pandas as pd
import streamlit as st
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import Resource
from rich.console import Console

DATA_API_SERVICE_NAME = "youtube"
DATA_API_VERSION = "v3"
ANALYTICS_API_SERVICE_NAME = "youtubeanalytics"
ANALYTICS_API_VERSION = "v2"


CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
    "https://www.googleapis.com/auth/youtube.force-ssl",
]
video_id = "xubQ0lsiV44"

console = Console()


@st.cache_resource
def authenticate() -> InstalledAppFlow:
    credentials = None

    if Path("token.pickle").exists():
        with open("token.pickle", "rb") as token:
            console.log("Loading Credentials from pickle")
            credentials = pickle.load(token)

    # Check token validity or login
    if not credentials or not credentials.valid:
        try:
            console.log("Refreshing Access Token...")
            credentials.refresh(Request())
        except:
            console.print("Fetching New Tokens...please authenticate in browser")
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE,
                scopes=SCOPES,
            )
            flow.run_local_server()
            credentials = flow.credentials

            with open("token.pickle", "wb") as f:
                console.log("Saving Token...")
                pickle.dump(credentials, f)

    return credentials


@st.cache_resource
def get_yt_data(_credentials: InstalledAppFlow) -> Resource:
    """Get Client to Youtube Data v3 API"""
    return build(
        DATA_API_SERVICE_NAME,
        DATA_API_VERSION,
        credentials=_credentials,
    )


@st.cache_data
def get_channel_id(_yt_data: Resource):
    channels_response = _yt_data.channels().list(mine=True, part="id").execute()
    channel_id = channels_response["items"][0][
        "id"
    ]  # I always assume there is only one ahah
    return channel_id


@st.cache_data
def get_videoid_to_topcomments(_yt_data, video_id, comments=None, token=""):
    if comments is None:
        comments = []

    video_response = (
        _yt_data.commentThreads()
        .list(part="id,snippet", videoId=video_id, pageToken=token)
        .execute()
    )

    for item in video_response["items"]:
        comments.append(item["snippet"]["topLevelComment"]["snippet"])

    if "nextPageToken" in video_response:
        return get_videoid_to_topcomments(
            _yt_data, video_id, comments, video_response["nextPageToken"]
        )
    else:
        return comments


def main():
    credentials = authenticate()
    console.print("Authenticated!")

    st.title("Streamlit Giveaway Table")

    yt_data = get_yt_data(credentials)

    channel_id = get_channel_id(yt_data)
    console.print(f"Analyzing for channel_id [yellow]{channel_id}")

    comments_response = get_videoid_to_topcomments(yt_data, video_id)

    df = pd.json_normalize(comments_response)

    congrats_placeholder = st.empty()
    table_placeholder = st.empty()

    table_placeholder.dataframe(
        df,
        hide_index=True,
        column_order=[
            "authorDisplayName",
            "authorProfileImageUrl",
            "textOriginal",
            "authorChannelId.value",
            "authorChannelUrl",
        ],
        column_config={
            "authorProfileImageUrl": st.column_config.ImageColumn(width="small"),
            "authorChannelUrl": st.column_config.LinkColumn(),
        },
    )

    all_participants = (
        df[["authorProfileImageUrl", "authorDisplayName"]]
        .drop_duplicates()
        .sort_values("authorDisplayName")
    )

    button_placeholder = st.empty()

    if button_placeholder.button("Sample winners", type="primary"):
        st.balloons()
        table_placeholder.dataframe(
            all_participants.sample(5, random_state=42),
            column_config={
                "authorProfileImageUrl": st.column_config.ImageColumn(width="small"),
            },
        )
        congrats_placeholder.success("Congratulations to the winners!", icon="🎈")
        button_placeholder.empty()


if __name__ == "__main__":
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    console.print("Running Giveaway", style="magenta")
    main()
