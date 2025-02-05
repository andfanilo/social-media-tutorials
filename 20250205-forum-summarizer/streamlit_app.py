"""
Before running, create .streamlit > secrets.toml file to contain OpenAI API key like:
OPENAI_API_KEY="sk-proj-XXX"
"""

from typing import List

import requests
import streamlit as st
import tiktoken
from bs4 import BeautifulSoup
from openai import OpenAI
from pydantic import BaseModel
from pydantic import computed_field

##################################################
### STREAMLIT INITIALIZATION
##################################################

st.set_page_config(page_title="Forum Summarizer")

if "generated_idea" not in st.session_state:
    st.session_state.generated_idea = ""

BASE_URL = "https://discuss.streamlit.io"

##################################################
### DEFINE PYDANTIC MODELS
##################################################


class Topic(BaseModel):
    id: int
    slug: str
    title: str

    @computed_field
    @property
    def url(self) -> str:
        return f"{BASE_URL}/t/{self.slug}/{self.id}.json"


class TopicList(BaseModel):
    topics: List[Topic]


class TopResponse(BaseModel):
    # Pydantic models won't error when you provide data for unrecognized fields
    # They will just be ignored
    topic_list: TopicList


class Post(BaseModel):
    id: int
    cooked: str
    accepted_answer: bool

    @computed_field
    @property
    def clean_text(self) -> str:
        soup = BeautifulSoup(self.cooked, "html.parser")
        return soup.get_text(separator=" ", strip=True)


class PostList(BaseModel):
    posts: List[Post]


class PostResponse(BaseModel):
    id: int
    fancy_title: str
    post_stream: PostList

    @computed_field
    @property
    def clean_post_stream(self) -> str:
        return "\n\n".join(
            f"Comment {i} - {p.clean_text}"
            for i, p in enumerate(self.post_stream.posts)
        )

    @computed_field
    @property
    def clean_post(self) -> str:
        return f"# Topic Title: {self.fancy_title} \n\n {self.clean_post_stream}"


##################################################
### QUERYING
##################################################


@st.cache_data
def count_tokens(prompt: str) -> int:
    """Approximate token count using tiktoken"""
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    return len(encoding.encode(prompt))


@st.cache_data
def get_top_topics():
    r = requests.get(f"{BASE_URL}/top.json?period=monthly")
    r.raise_for_status()
    return TopResponse.model_validate(r.json())


@st.cache_data
def get_post(url: str):
    r = requests.get(url)
    r.raise_for_status()
    return PostResponse.model_validate(r.json())


def generate_full_prompt(all_topics: TopResponse, number_posts: int = 40) -> str:
    prompt_prefix = """Analyze the following forum topics and comments to:
    1. Identify the top 5 pain points users are experiencing
    2. Suggest potential solutions for each pain point
    3. Prioritize them by frequency of mention
    """
    forum_content = "\n\n".join(
        [
            get_post(topic.url).clean_post
            for topic in all_topics.topic_list.topics[:number_posts]
        ]
    )
    return "\n\n".join([prompt_prefix, forum_content])


def generate_callback(full_prompt):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    response = client.chat.completions.create(
        model="gpt-4o", messages=[{"role": "user", "content": full_prompt}]
    )
    st.session_state.generated_idea = response.choices[0].message.content


##################################################
### USER INTERFACE
##################################################

st.title("💡 Pain Points Summarizer from latest Streamlit Forum posts")

top_topics = get_top_topics()

with st.expander(f"List {len(top_topics.topic_list.topics)} posts data"):
    selected_url = st.selectbox(
        "Select URL",
        [topic.url for topic in top_topics.topic_list.topics],
    )
    post_data = get_post(selected_url)

    st.markdown(post_data.clean_post)

full_prompt = generate_full_prompt(top_topics)
token_count = count_tokens(full_prompt)

tiktoken_disclaimer_column, submit_button_column = st.columns(
    (3, 1), vertical_alignment="center"
)
tiktoken_disclaimer_column.write(
    f"Generation will consume approx. {token_count} tokens"
)
submit_button_column.button(
    "Generate ideas",
    type="primary",
    use_container_width=True,
    on_click=generate_callback,
    args=(full_prompt,),
)

if st.session_state.generated_idea:
    st.markdown(st.session_state.generated_idea)
