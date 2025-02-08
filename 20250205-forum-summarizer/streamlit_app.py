"""
Before running, create .streamlit > secrets.toml file to contain OpenAI API key like:
OPENAI_API_KEY="sk-proj-XXX"
"""

from typing import Dict
from typing import List
from typing import Optional
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

if "generated_summary" not in st.session_state:
    st.session_state.generated_summary = ""

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


class PainPointDetails(BaseModel):
    details: str
    python_code_example: str


class SolutionDetails(BaseModel):
    details: str
    python_code_example: str


class PainPoint(BaseModel):
    hook: str
    summary_explanation: str
    detailed_explanation: Optional[PainPointDetails]
    solution: Optional[SolutionDetails]


class OpenAIResponse(BaseModel):
    abstract: str
    pain_point_1: PainPoint
    pain_point_2: PainPoint
    pain_point_3: PainPoint
    pain_point_4: PainPoint
    pain_point_5: PainPoint


##################################################
### QUERYING
##################################################


@st.cache_data
def query_forum(url: str) -> Dict:
    r = requests.get(url)
    r.raise_for_status()
    return r.json()


def get_top_topics() -> TopResponse:
    data = query_forum(f"{BASE_URL}/top.json?period=monthly")
    return TopResponse.model_validate(data)


def get_post(url: str) -> PostResponse:
    data = query_forum(url)
    return PostResponse.model_validate(data)


def download_all_top_posts(all_topics: TopResponse) -> List[PostResponse]:
    number_posts = len(all_topics.topic_list.topics)
    progress_bar = st.progress(0, text="Downloading")

    def download_post(idx, topic) -> PostResponse:
        progress_bar.progress(idx / number_posts, text=f"Downloading **{topic.title}**")
        return get_post(topic.url)

    all_posts = [
        download_post(idx, topic)
        for idx, topic in enumerate(all_topics.topic_list.topics)
    ]
    progress_bar.empty()
    return all_posts


@st.cache_data
def count_tokens(prompt: str) -> int:
    """Approximate token count using tiktoken"""
    encoding = tiktoken.get_encoding("cl100k_base")  # GPT-4 encoding
    return len(encoding.encode(prompt))


def generate_full_prompt(all_posts: List[PostResponse], number_posts: int = 50) -> str:
    prompt_prefix = """Analyze the following forum topics and comments to:
    1. Identify the top 5 pain points users are experiencing
    2. Suggest potential solutions for each pain point
    3. Prioritize them by frequency of mention
    """
    forum_content = "\n\n".join([post.clean_post for post in all_posts[:number_posts]])
    return "\n\n".join([prompt_prefix, forum_content])


def submit_openai_callback(content):
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
    with st.spinner("Generating summary..."):
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[{"role": "user", "content": content}],
            response_format=OpenAIResponse,
        )
    generated_summary = completion.choices[0].message
    if generated_summary.refusal:
        raise ValueError("Problem in OpenAI generation, try again")
    else:
        st.session_state.generated_summary = generated_summary.parsed


##################################################
### USER INTERFACE
##################################################

st.title("💡 Summarizer from Monthly Top Streamlit Forum")

top_topics = get_top_topics()
all_posts = download_all_top_posts(top_topics)

with st.expander(f"List {len(all_posts)} posts data"):
    all_posts_details = {post.fancy_title: post.clean_post_stream for post in all_posts}
    selected_post = st.selectbox(
        "Select Post",
        all_posts_details.keys(),
    )
    st.markdown(all_posts_details.get(selected_post))


number_posts = st.slider("How many posts to summarize?", 1, len(all_posts), 25)
full_prompt = generate_full_prompt(all_posts, number_posts)
token_count = count_tokens(full_prompt)


tiktoken_disclaimer_column, submit_button_column = st.columns(
    (3, 1), vertical_alignment="center"
)
tiktoken_disclaimer_column.write(
    f"Generation will consume approx. {token_count} tokens"
)
submit_summary = submit_button_column.button(
    "Generate ideas",
    type="primary",
    use_container_width=True,
    on_click=submit_openai_callback,
    args=(full_prompt,),
)

if st.session_state.generated_summary:
    generated_summary: OpenAIResponse = st.session_state.generated_summary

    st.header("Summary")
    st.write(generated_summary.abstract)

    for pain_point in [f"pain_point_{i}" for i in range(1, 6)]:
        point = getattr(generated_summary, pain_point)
        st.subheader(point.hook)
        st.markdown(point.summary_explanation)

        if point.detailed_explanation:
            st.markdown(":blue[**Details**]")
            st.write(point.detailed_explanation.details)
            st.code(point.detailed_explanation.python_code_example)
        if point.solution:
            st.markdown(":green[**Solution**]")
            st.write(point.solution.details)
            st.code(point.solution.python_code_example)
