import pandas as pd
import plotly.express as px
import streamlit as st

#################################################
### DATA
#################################################


@st.cache_data(max_entries=5)
def load_data(path: str):
    data = pd.read_csv(
        path,
        parse_dates=["Date Sumbited", "Date Received"],
    )
    data = data.rename(columns={"Date Sumbited": "Date Submitted"})
    return data


@st.cache_data
def transform_data(data, selected_products, selected_date):
    if selected_products:
        data = data[data["Product"].isin(selected_products)]
    if selected_date:
        data = data[data["Date Submitted"].dt.date == selected_date]
    return data


df = load_data("./data/Financial Consumer Complaints.csv")

all_products = df["Product"].unique()

#################################################
### UI
#################################################

st.title("📞 What are the usual failing products?")

with st.expander("**Configuration**", icon="⚙"):
    left_filter, right_filter = st.columns(2, gap="medium")

with left_filter:
    selected_products = st.multiselect(
        "Select a product",
        all_products,
        None,
    )
    st.session_state.options = selected_products
with right_filter:
    selected_date = st.date_input(
        "Select a date",
        None,
        min_value=df["Date Submitted"].min(),
        max_value=df["Date Submitted"].max(),
    )

filtered_df = transform_data(df, selected_products, selected_date)

count_number_complaints = len(filtered_df)
count_disputes = len(filtered_df[filtered_df["Consumer disputed?"] == "Yes"])
count_complaints_by_product = (
    filtered_df.groupby(["Date Submitted", "Product"])
    .agg(Count=("Product", "count"))
    .reset_index()
)
count_complaints_by_subproducts = (
    filtered_df.groupby(["Sub-product"])
    .agg(Count=("Sub-product", "count"))
    .reset_index()
)


row_metrics = st.columns(2)

with row_metrics[0]:
    with st.container(border=True):
        st.metric(
            "Number of complaints",
            count_number_complaints,
            delta=f"{1} % since last week",
        )
with row_metrics[1]:
    with st.container(border=True):
        st.metric(
            "Number of disputes",
            count_disputes,
            delta=f"{-1} % since last week",
        )


fig_complaints_by_product = px.line(
    count_complaints_by_product,
    x="Date Submitted",
    y="Count",
    color="Product",
)
fig_complaints_by_sub_product = px.bar(
    count_complaints_by_subproducts,
    x="Count",
    y="Sub-product",
    orientation="h",
)
fig_complaints_by_sub_product.update_layout(
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)


row_charts = st.columns((2, 1))

with row_charts[0]:
    st.plotly_chart(fig_complaints_by_product)

with row_charts[1]:
    st.plotly_chart(fig_complaints_by_sub_product)


st.dataframe(df, hide_index=True)
