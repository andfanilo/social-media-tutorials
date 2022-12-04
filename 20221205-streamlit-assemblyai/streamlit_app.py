import logging
import os
import tempfile
from io import BytesIO
from typing import Dict

import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import yaml
from faker import Faker
from pydub import AudioSegment
from st_aggrid import AgGrid
from streamlit_chat import message as st_message
from streamlit_option_menu import option_menu
from yaml import SafeLoader

import utils

logger = logging.getLogger(__name__)
fake = Faker()

parent_dir = os.path.dirname(os.path.abspath(__file__))
build_dir = os.path.join(
    parent_dir, "streamlit_audio_recorder/st_audiorec/frontend/build"
)
st_audiorec = components.declare_component("st_audiorec", path=build_dir)


# https://github.com/AssemblyAI-Examples/assemblyai-and-python-in-5-minutes/blob/main/transcribe.py
def send_to_assemblyai(raw_audio: Dict) -> Dict:
    """Send raw_audio from st_audiorec to AssemblyAI
    Store transcript response in session state
    """
    api_key = st.secrets["assemblyai"]["key"]
    header = {"authorization": api_key, "content-type": "application/json"}

    ind, val = zip(*raw_audio["arr"].items())
    ind = np.array(ind, dtype=int)
    val = np.array(val)
    sorted_ints = val[ind]
    stream = BytesIO(b"".join([int(v).to_bytes(1, "big") for v in sorted_ints]))
    audio = AudioSegment.from_file(stream, format="wav")

    with tempfile.NamedTemporaryFile(suffix=".wav") as path_to_file:
        audio.export(path_to_file, format="wav")
        logger.info(f"Created file in {path_to_file.name}")
        upload_url = utils.upload_file(path_to_file.name, header)
        transcript_response = utils.request_transcript(upload_url, header)
        polling_endpoint = utils.make_polling_endpoint(transcript_response)
        utils.wait_for_completion(polling_endpoint, header)
        paragraphs = utils.get_paragraphs(polling_endpoint, header)

    st.session_state.transcript = paragraphs


def generate_chatbot_answer(text: str):
    """Add user message and chatbot message to session state"""
    st.session_state.history.append({"message": text, "is_user": True})
    st.session_state.history.append({"message": fake.text(), "is_user": False})


def about():
    st.header("Transcribe and understand audio with a single AI-powered API")
    st.markdown(
        "Automatically convert audio and video files and live audio streams to text with AssemblyAI's Speech-to-Text APIs. Do more with Audio Intelligence - summarization, content moderation, topic detection, and more. Powered by cutting-edge AI models."
    )


def app():
    col1, _, col2 = st.columns((1, 0.1, 1))

    with col2:
        st.subheader("Chatbot")

        for chat in st.session_state.history:
            st_message(**chat, key=chat["message"])

    with col1:
        st.subheader("Transcriber")
        raw_audio = st_audiorec()
        if not isinstance(raw_audio, dict):
            st.stop()

        st.button(
            "Transcribe with Assembly AI",
            on_click=send_to_assemblyai,
            args=(raw_audio,),
        )

        if len(st.session_state.transcript) == 0:
            st.stop()

        # st.json(st.session_state.transcript[0])
        words = pd.DataFrame.from_records(st.session_state.transcript[0]["words"])
        edited_words = AgGrid(words[["text", "confidence"]], editable=True)
        edited_sentence = " ".join(edited_words["data"]["text"].values)

        st.button(
            "Submit to Chatbot",
            type="primary",
            on_click=generate_chatbot_answer,
            args=(edited_sentence,),
        )


def main():
    with open("./.streamlit/users.yaml") as file:
        users_config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        users_config["credentials"],
        users_config["cookie"]["name"],
        users_config["cookie"]["key"],
    )

    name, authentication_status, _ = authenticator.login("Login", "main")

    if authentication_status:
        with st.sidebar:
            selected_page = option_menu(
                "Main Menu",
                ["About", "App", "Resources"],
                icons=["book", "house", "link"],
                menu_icon="cast",
                default_index=1,
            )
        st.sidebar.info(f"Welcome {name}!")
        authenticator.logout(f"Logout", "sidebar")

    elif authentication_status == False:
        st.error("Username/password is incorrect")
        st.stop()
    elif authentication_status == None:
        st.warning("Please enter your username and password")
        st.stop()

    pages = {
        "About": about,
        "App": app,
        "Resources": about,
    }

    pages[selected_page]()


if __name__ == "__main__":
    st.set_page_config(
        page_title="Assembly AI Demo", page_icon=":robot:", layout="wide"
    )
    st.title("My Vocal Chatbot")
    st.sidebar.header("Configuration")

    if "history" not in st.session_state:
        st.session_state.history = []

    if "transcript" not in st.session_state:
        st.session_state.transcript = []

    main()
