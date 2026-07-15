import html
import io
import re

import pandas as pd
import requests
import soundfile as sf
import streamlit as st
from datasets import Audio, load_dataset
from sklearn.datasets import load_digits
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Pagination Demos", layout="wide")

st.html("<style>.stMainBlockContainer { padding-top: 3rem; }</style>")


# ---------------------------------------------------------------------------
# Dataframe pagination
# ---------------------------------------------------------------------------
def dataframe_demo():
    st.title("Paginate a Dataframe")
    st.caption("Superstore 2024 sales data, sliced into pages of rows with `st.pagination`.")

    df = pd.read_csv("data/Superstore_2024.csv")
    rows_per_page = 3
    total_pages = (len(df) + rows_per_page - 1) // rows_per_page

    # Use placeholders to show dataframe above pagination
    dataframe_slot = st.empty()
    page = st.pagination(
        num_pages=total_pages,
        max_visible_pages=15,
        bind="query-params",
        key="selected_page",
    )

    start_idx = (page - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    dataframe_slot.dataframe(df.iloc[start_idx:end_idx], hide_index=True)


# ---------------------------------------------------------------------------
# API results
# ---------------------------------------------------------------------------
HN_API_URL = "https://hacker-news.firebaseio.com/v0"
COMMENTS_PER_PAGE = 3


def clean_hn_comment_text(raw_html: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw_html)
    return html.unescape(text).strip()


@st.cache_data(show_spinner=False)
def fetch_hn_item(item_id: int) -> dict:
    response = requests.get(f"{HN_API_URL}/item/{item_id}.json", timeout=10)
    response.raise_for_status()
    return response.json()


@st.cache_data(show_spinner="Fetching top stories from Hacker News...")
def fetch_top_stories(limit: int = 15) -> list[dict]:
    response = requests.get(f"{HN_API_URL}/topstories.json", timeout=10)
    response.raise_for_status()
    story_ids = response.json()[:limit]
    return [fetch_hn_item(story_id) for story_id in story_ids]


def api_results_demo():
    st.title("Paginate API Results")
    st.caption(
        "Backed by the live Hacker News API. Pick a story, then page through "
        "its top-level comments, each extracted and shown as a chat bubble."
    )

    stories = fetch_top_stories()
    story = st.selectbox(
        "Story",
        stories,
        format_func=lambda s: f"{s.get('title', '(untitled)')} ({s.get('descendants', 0)} comments)",
    )

    comment_ids = story.get("kids", [])
    total_pages = max(1, -(-len(comment_ids) // COMMENTS_PER_PAGE))
    results_slot = st.empty()
    with st.container(horizontal_alignment="right"):
        # Keyed per-story so switching stories resets to page 1 instead of
        # reusing a page number that may be out of range for the new story.
        page = st.pagination(num_pages=total_pages, key=f"api_page_{story['id']}")

    start = (page - 1) * COMMENTS_PER_PAGE
    page_comment_ids = comment_ids[start : start + COMMENTS_PER_PAGE]
    with results_slot.container():
        if not page_comment_ids:
            st.info("This story has no comments yet.")
        for comment_id in page_comment_ids:
            comment = fetch_hn_item(comment_id)
            author = comment.get("by", "[deleted]")
            text = clean_hn_comment_text(comment.get("text", "*[deleted]*"))
            with st.chat_message(name="user"):
                st.markdown(f"**{author}**")
                st.write(text)


# ---------------------------------------------------------------------------
# Image gallery
# ---------------------------------------------------------------------------
IMAGES_PER_PAGE = 6
TOTAL_IMAGES = 60
# Picsum's low ids (0-5ish) happen to all be laptop/desk photos, and not
# every id up to ~1084 is actually valid (some 404 with "Image does not
# exist"). Pull the real id list and multiply by a prime to scatter picks
# across it instead of walking it in order.
PICSUM_ID_SEED = 37


@st.cache_data(show_spinner=False)
def fetch_picsum_ids() -> list[int]:
    ids = []
    page = 1
    while True:
        response = requests.get("https://picsum.photos/v2/list", params={"page": page, "limit": 100}, timeout=10)
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        ids.extend(int(item["id"]) for item in batch)
        page += 1
    return ids


def image_gallery_demo():
    st.title("Paginate an Image Gallery")
    st.caption("Random photos from Picsum, six per page in a responsive grid.")

    total_pages = -(-TOTAL_IMAGES // IMAGES_PER_PAGE)
    gallery_slot = st.empty()
    with st.container(horizontal_alignment="right"):
        page = st.pagination(num_pages=total_pages, key="gallery_page")

    valid_ids = fetch_picsum_ids()
    start_index = (page - 1) * IMAGES_PER_PAGE
    with gallery_slot.container():
        cols = st.columns(3)
        for offset, index in enumerate(range(start_index, start_index + IMAGES_PER_PAGE)):
            image_id = valid_ids[(index * PICSUM_ID_SEED) % len(valid_ids)]
            with cols[offset % 3]:
                st.image(f"https://picsum.photos/id/{image_id}/600/400", caption=f"Photo #{image_id}")


# ---------------------------------------------------------------------------
# Model inference review (handwritten digits)
# ---------------------------------------------------------------------------
DIGITS_TEST_SIZE = 0.25
DIGITS_TOP_N_CLASSES = 5

# Emphasis form: one accent hue for the top prediction, gray for context bars.
# Colors are the validated light/dark steps from the dataviz skill's reference palette.
CHART_COLORS = {
    "light": {"accent": "#2a78d6", "context": "#c3c2b7", "text": "#0b0b0b", "surface": "#fcfcfb"},
    "dark": {"accent": "#3987e5", "context": "#383835", "text": "#ffffff", "surface": "#1a1a19"},
}


@st.cache_resource(show_spinner="Training a digit-recognition model...")
def train_digit_classifier():
    digits = load_digits()
    x_train, x_test, y_train, y_test, _, test_indices = train_test_split(
        digits.data,
        digits.target,
        range(len(digits.target)),
        test_size=DIGITS_TEST_SIZE,
        stratify=digits.target,
        random_state=42,
    )
    model = LogisticRegression(max_iter=2000)
    model.fit(x_train, y_train)
    return model, digits.images, x_test, y_test, list(test_indices)


def build_confidence_chart_data(probabilities, theme: str) -> pd.DataFrame:
    colors = CHART_COLORS[theme]
    top_indices = probabilities.argsort()[::-1][:DIGITS_TOP_N_CLASSES]
    top_probs = probabilities[top_indices] * 100
    bar_colors = [colors["accent"] if i == 0 else colors["context"] for i in range(len(top_indices))]
    return pd.DataFrame({"digit": [str(i) for i in top_indices], "confidence": top_probs, "color": bar_colors})


def confirm_digit_prediction(sample_index: int) -> None:
    confirmed = st.session_state.setdefault("confirmed_predictions", set())
    confirmed.add(sample_index)


def submit_reviewed_digit(sample_index: int, review_key: str) -> None:
    confirmed = st.session_state.setdefault("confirmed_predictions", set())
    confirmed.add(sample_index)
    reviewed = st.session_state.setdefault("reviewed_digits", {})
    reviewed[sample_index] = st.session_state[review_key]


def model_inference_demo():
    st.title("Paginate Model Inference Review")
    st.caption(
        "A logistic regression classifier trained on scikit-learn's handwritten "
        "digits dataset. Page through held-out test digits, review the model's "
        "top predicted classes with confidence, then confirm."
    )

    model, images, x_test, y_test, test_indices = train_digit_classifier()
    total_pages = len(y_test)
    review_slot = st.empty()
    page = st.container(horizontal_alignment="right").pagination(num_pages=total_pages, key="digits_page")

    sample_index = page - 1
    image_index = test_indices[sample_index]
    probabilities = model.predict_proba([x_test[sample_index]])[0]
    predicted_class = probabilities.argmax()
    true_class = y_test[sample_index]

    theme = st.context.theme.type
    confirmed = st.session_state.setdefault("confirmed_predictions", set())

    review_container = review_slot.container()

    media_row = review_container.container(horizontal=True, vertical_alignment="center", gap="small")
    media_row.image(images[image_index] / 16.0, caption=f"True digit: {true_class}", width=150, clamp=True)
    media_row.bar_chart(
        build_confidence_chart_data(probabilities, theme),
        x="digit",
        y="confidence",
        color="color",
        horizontal=True,
        sort=False,
        x_label="",
        y_label="Confidence (%)",
        width=250,
        height=150,
    )

    review_container.write(f"Predicted: **{predicted_class}** ({probabilities[predicted_class] * 100:.0f}% confidence)")

    review_key = f"review_digit_{sample_index}"
    action_row = review_container.container(horizontal=True, vertical_alignment="bottom", gap="large")
    action_row.button(
        "Confirm",
        key=f"confirm_{sample_index}",
        type="primary",
        width=150,
        on_click=confirm_digit_prediction,
        args=(sample_index,),
    )

    review_form = action_row.form("review_form", border=False)
    review_row = review_form.container(horizontal=True, vertical_alignment="bottom", gap="small")
    review_row.number_input(
        "or review digit",
        min_value=0,
        max_value=9,
        value=int(predicted_class),
        step=1,
        key=review_key,
        width=150,
    )
    review_row.form_submit_button(
        "Submit",
        on_click=submit_reviewed_digit,
        args=(sample_index, review_key),
    )

    if sample_index in confirmed:
        action_row.write("✅ Checked")


# ---------------------------------------------------------------------------
# Hugging Face audio dataset review
# ---------------------------------------------------------------------------
AUDIO_DATASET = "hf-internal-testing/librispeech_asr_dummy"
AUDIO_CONFIG = "clean"
AUDIO_SPLIT = "validation"
CLIPS_PER_PAGE = 1


@st.cache_resource(show_spinner="Loading audio dataset into memory...")
def load_audio_dataset():
    dataset = load_dataset(AUDIO_DATASET, AUDIO_CONFIG, split=AUDIO_SPLIT)
    # decode=False keeps raw bytes on the dataset object instead of eagerly
    # decoding every clip; we decode per-clip with soundfile below.
    return dataset.cast_column("audio", Audio(decode=False))


def submit_transcript(sample_id: str, transcript_key: str, current_page: int, total_pages: int) -> None:
    submitted = st.session_state.setdefault("submitted_transcripts", {})
    submitted[sample_id] = st.session_state[transcript_key]
    if current_page < total_pages:
        st.session_state["audio_page"] = current_page + 1


def audio_review_demo():
    st.title("Paginate a Hugging Face Audio Dataset")
    st.caption(
        f"`{AUDIO_DATASET}` is downloaded once via the `datasets` library and "
        "held in memory. Pagination then just slices the in-memory dataset."
    )

    dataset = load_audio_dataset()
    total_pages = -(-len(dataset) // CLIPS_PER_PAGE)
    clips_slot = st.empty()
    page = st.container(horizontal_alignment="right").pagination(num_pages=total_pages, key="audio_page")

    start = (page - 1) * CLIPS_PER_PAGE
    clips_container = clips_slot.container()
    for i in range(start, min(start + CLIPS_PER_PAGE, len(dataset))):
        sample = dataset[i]
        audio_data, sample_rate = sf.read(io.BytesIO(sample["audio"]["bytes"]))
        clips_container.write(f"**{sample['id']}**, speaker `{sample['speaker_id']}`")
        clips_container.caption(sample["text"].capitalize())
        clips_container.audio(audio_data, sample_rate=sample_rate)

        submitted_transcripts = st.session_state.setdefault("submitted_transcripts", {})
        transcript_key = f"transcription_{sample['id']}"
        default_transcript = submitted_transcripts.get(sample["id"], sample["text"].capitalize())
        clips_container.text_area("Review transcript", value=default_transcript, key=transcript_key)

        action_row = clips_container.container(horizontal=True, vertical_alignment="center", gap="large")
        action_row.button(
            "Submit",
            key=f"submit_{sample['id']}",
            type="primary",
            width=120,
            on_click=submit_transcript,
            args=(sample["id"], transcript_key, page, total_pages),
        )
        if sample["id"] in submitted_transcripts:
            action_row.write("✅ Checked")
        clips_container.divider()


# ---------------------------------------------------------------------------
# Search results (dynamic num_pages)
# ---------------------------------------------------------------------------
GITHUB_REPO = "streamlit/streamlit"
GITHUB_MAX_SEARCH_RESULTS = 1000  # GitHub search caps at 1000 results per query
SEARCH_RESULTS_PER_PAGE = 6
SEARCH_RESULTS_COLUMNS = 3


@st.cache_data(show_spinner="Searching GitHub issues...")
def search_github_issues(query: str, page: int, per_page: int) -> dict:
    response = requests.get(
        "https://api.github.com/search/issues",
        params={"q": f"repo:{GITHUB_REPO} {query}".strip(), "per_page": per_page, "page": page},
        headers={"Accept": "application/vnd.github+json"},
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def search_results_demo():
    st.title("Paginate Search Results")
    st.caption(
        f"Search issues and PRs in `{GITHUB_REPO}`. The result count (and so "
        "`num_pages`) recomputes on every keystroke, matching the dynamic-"
        "`num_pages` case called out in streamlit/streamlit#14975's review."
    )

    query = st.text_input("Search issues", placeholder="e.g. 'pagination', 'st.chat_input'")
    first_page = search_github_issues(query, page=1, per_page=SEARCH_RESULTS_PER_PAGE)
    total_results = min(first_page["total_count"], GITHUB_MAX_SEARCH_RESULTS)
    total_pages = max(1, -(-total_results // SEARCH_RESULTS_PER_PAGE))

    results_slot = st.empty()
    with st.container(horizontal_alignment="right"):
        page = st.pagination(num_pages=total_pages, key="search_page")

    results = first_page if page == 1 else search_github_issues(query, page=page, per_page=SEARCH_RESULTS_PER_PAGE)
    with results_slot.container():
        st.write(f"{first_page['total_count']} result(s)")
        items = results["items"]
        for row_start in range(0, len(items), SEARCH_RESULTS_COLUMNS):
            row_items = items[row_start : row_start + SEARCH_RESULTS_COLUMNS]
            cols = st.columns(SEARCH_RESULTS_COLUMNS)
            for col, item in zip(cols, row_items):
                with col, st.container(border=True, height="stretch"):
                    kind = "PR" if "pull_request" in item else "Issue"
                    state_icon = "🟢" if item["state"] == "open" else "🟣"
                    st.markdown(f"{state_icon} **[{kind} #{item['number']}]({item['html_url']}): {item['title']}**")
                    st.caption(f"by {item['user']['login']} · {item['comments']} comments")


# ---------------------------------------------------------------------------
# Navigation
# ---------------------------------------------------------------------------
pages = [
    st.Page(dataframe_demo, title="Dataframe", icon="🗂️", default=True),
    st.Page(api_results_demo, title="API Results", icon="🌐"),
    st.Page(audio_review_demo, title="Audio Review", icon="🎧"),
    st.Page(image_gallery_demo, title="Image Gallery", icon="🖼️"),
    st.Page(model_inference_demo, title="Model Inference", icon="🤖"),
    st.Page(search_results_demo, title="Search Results", icon="🔍"),
]

pg = st.navigation(pages)
pg.run()
