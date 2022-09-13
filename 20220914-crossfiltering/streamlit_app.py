import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st

from typing import Dict
from typing import Set
from streamlit_plotly_events import plotly_events


@st.experimental_singleton
def load_data() -> pd.DataFrame:
    return px.data.tips()


def initialize_state():
    """Initializes all filters and counter in Streamlit Session State
    """
    for q in ["bill_to_tip", "size_to_time", "day"]:
        if f"{q}_query" not in st.session_state:
            st.session_state[f"{q}_query"] = set()

    if "counter" not in st.session_state:
        st.session_state.counter = 0


def reset_state_callback():
    """Resets all filters and increments counter in Streamlit Session State
    """
    st.session_state.counter = 1 + st.session_state.counter

    for q in ["bill_to_tip", "size_to_time", "day"]:
        st.session_state[f"{q}_query"] = set()


def query_data(df: pd.DataFrame) -> pd.DataFrame:
    """Apply filters in Streamlit Session State
    to filter the input DataFrame
    """
    df["bill_to_tip"] = (
        (100 * df["total_bill"]).astype(int).astype(str)
        + "-"
        + (100 * df["tip"]).astype(int).astype(str)
    )
    df["size_to_time"] = df["size"].astype(str) + "-" + df["time"].astype(str)
    df["selected"] = True

    for q in ["bill_to_tip", "size_to_time", "day"]:
        if st.session_state[f"{q}_query"]:
            df.loc[~df[q].isin(st.session_state[f"{q}_query"]), "selected"] = False

    return df


def build_bill_to_tip_figure(df: pd.DataFrame) -> go.Figure:
    fig = px.scatter(
        df,
        "total_bill",
        "tip",
        color="selected",
        color_discrete_sequence=["rgba(99, 110, 250, 0.2)", "rgba(99, 110, 250, 1)"],
        category_orders={"selected": [False, True]},
        hover_data=[
            "total_bill",
            "tip",
            "day",
        ],
        height=800,
    )
    fig.update_layout(paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF")
    fig.update_xaxes(gridwidth=0.1, gridcolor="#EDEDED")
    fig.update_yaxes(gridwidth=0.1, gridcolor="#EDEDED")
    return fig


def build_size_to_time_figure(df: pd.DataFrame) -> go.Figure:
    return px.density_heatmap(df[df["selected"] == True], "size", "time", height=400)


def build_day_figure(df: pd.DataFrame) -> go.Figure:
    return px.histogram(
        df,
        "day",
        color="selected",
        color_discrete_sequence=["rgba(99, 110, 250, 1)", "rgba(99, 110, 250, 0.2)"],
        category_orders={
            "selected": [True, False],
            "day": ["Thur", "Fri", "Sat", "Sun"],
        },
        height=400,
    )


def render_preview_ui(df: pd.DataFrame):
    """Renders an expander with content of DataFrame and Streamlit Session State
    """
    with st.expander("Preview"):
        l, r = st.columns(2)
        l.dataframe(
            df,
        )
        r.json(
            {
                k: v
                for k, v in st.session_state.to_dict().items()
                if f'_{st.session_state["counter"]}' not in k
            }
        )


def render_plotly_ui(transformed_df: pd.DataFrame) -> Dict:
    """Renders all Plotly figures.

    Returns a Dict of filter to set of row identifiers to keep, built from the
    click/select events from Plotly figures.

    The return will be then stored into Streamlit Session State next.
    """
    c1, c2 = st.columns(2)

    bill_to_tip_figure = build_bill_to_tip_figure(transformed_df)
    size_to_time_figure = build_size_to_time_figure(transformed_df)
    day_figure = build_day_figure(transformed_df)

    with c1:
        bill_to_tip_selected = plotly_events(
            bill_to_tip_figure,
            select_event=True,
            key=f"bill_to_tip_{st.session_state.counter}",
        )
    with c2:
        size_to_time_clicked = plotly_events(
            size_to_time_figure,
            click_event=True,
            key=f"size_to_time_{st.session_state.counter}",
        )
        day_clicked = plotly_events(
            day_figure,
            click_event=True,
            key=f"day_{st.session_state.counter}",
        )

    current_query = {}
    current_query["bill_to_tip_query"] = {
        f"{int(100*el['x'])}-{int(100*el['y'])}" for el in bill_to_tip_selected
    }
    current_query["size_to_time_query"] = {
        f"{el['x']}-{el['y']}" for el in size_to_time_clicked
    }
    current_query["day_query"] = {el["x"] for el in day_clicked}

    return current_query


def update_state(current_query: Dict[str, Set]):
    """Stores input dict of filters into Streamlit Session State.

    If one of the input filters is different from previous value in Session State, 
    rerun Streamlit to activate the filtering and plot updating with the new info in State.
    """
    rerun = False
    for q in ["bill_to_tip", "size_to_time", "day"]:
        if current_query[f"{q}_query"] - st.session_state[f"{q}_query"]:
            st.session_state[f"{q}_query"] = current_query[f"{q}_query"]
            rerun = True

    if rerun:
        st.experimental_rerun()


def main():
    df = load_data()
    transformed_df = query_data(df)

    st.title("Plotly events")
    render_preview_ui(transformed_df)

    current_query = render_plotly_ui(transformed_df)

    update_state(current_query)

    st.button("Reset filters", on_click=reset_state_callback)


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    initialize_state()
    main()