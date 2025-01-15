import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.title("Pandas Pivot Table Practice")

##########################################
### READ
##########################################

st.header("0. Read Excel Data")

df = pd.read_excel(
    "data/Excel-Practice-Data-for-Pivot-Table-1.xlsx",
    sheet_name="Problem",
    skiprows=3,
    usecols="B:H",
    dtype={"Year": str},
)
df["Tax"] = df["Amount"] * 0.05
st.dataframe(df)

##########################################
### Pivot Table
##########################################

st.header("1. Pivot Table by Client")

pivot = pd.pivot_table(
    df,
    index="Client",  # group lines by
    values="Amount",  # which column to aggregate on
    aggfunc="sum",  # how to aggregate
    sort=True,  # sort Index, true by default
)
st.dataframe(pivot.sort_values("Amount", ascending=False))

# Clients grouped as first-level index, you can select by label
st.dataframe(pivot.loc["ABC Corporation"])
st.metric("Earnings of ABC Corporation", f"{pivot.loc['ABC Corporation'].item():,d} $")

# Multiple selection
st.dataframe(pivot.loc[["ABC Corporation", "Eagle Security"]])
st.dataframe(pivot.loc["A":"E"])
st.dataframe(pivot.loc[[True, False, False, False, True, False, False]])
st.dataframe(pivot.loc[lambda data: data.index.str.endswith("Company")])

# Plot index as x, Amount as y
st.plotly_chart(
    px.bar(pivot, x=None, y="Amount"),
    key="basic_chart",
)

# Some charting libraries don't read dataframe index
# Extract index as a new column
st.dataframe(pivot.reset_index())
st.plotly_chart(
    px.bar(pivot.reset_index(), x="Client", y="Amount"),
    key="basic_chart_reset_index",
)

##########################################
### Row MultiIndex
##########################################

st.header("2. Grouping Data by Client and Year")

pivot = pd.pivot_table(
    df,
    index=["Year", "Client"],
    values="Amount",
    aggfunc="sum",
)
st.dataframe(pivot)

# Selecting by Index
st.dataframe(pivot.loc["2019"])
st.dataframe(pivot.loc["2019"].loc["ABC Corporation"])
st.dataframe(pivot.loc[("2019", "ABC Corporation")])
st.metric(
    "Earnings of ABC Corporation in 2019",
    f"{pivot.loc[('2019', 'ABC Corporation')].item():,d} $",
)

st.dataframe(pivot.loc[("2019", "ABC Corporation"), :])  # always add a column indexer

# All selection options like slicing still possible
st.dataframe(pivot.loc["2019":"2020", :])
st.dataframe(pivot.loc[("2019", "ABC Corporation") : ("2020", "Eagle Security"), :])

# Selecting on the deeper Client level (not in video)
st.dataframe(pivot.swaplevel().loc["ABC Corporation", :])

# I don't want to swap levels and reorder though...
# Cross-section to make specific value selections per level
# (not in video)
st.dataframe(pivot.xs("ABC Corporation", level="Client"))

# Multiindex Slicer is the generic way for multilevel custom selection
# PS: Need to specify column selection in those examples
idx = pd.IndexSlice
st.dataframe(pivot.loc[idx[:, "ABC Corporation"], :])
st.dataframe(pivot.loc[idx["2019":"2020", "A":"E"], :])
st.dataframe(
    pivot.loc[
        idx[
            pivot.index.get_level_values("Year").astype(int) % 2 == 0,
            pivot.index.get_level_values("Client").str.endswith("Corporation"),
        ],
        :,
    ]
)

# More levels for fun
harder_pivot = pd.pivot_table(
    df,
    index=["Year", "Quarter", "Month", "Client"],
    values="Amount",
    aggfunc="sum",
)
st.dataframe(harder_pivot)
st.dataframe(
    harder_pivot.loc[
        idx[
            ["2020", "2022"],
            harder_pivot.index.get_level_values("Quarter").str[-1].astype(int) % 2 != 0,
            :,
            harder_pivot.index.get_level_values("Client").str.endswith("Corporation"),
        ],
    ]
)

# Charting
st.dataframe(pivot.reset_index("Year"))
st.bar_chart(pivot.reset_index("Year"), x=None, y="Amount", color="Year", stack=False)
st.bar_chart(pivot.reset_index(), x="Year", y="Amount", color="Client", stack=False)

# Try Mitosheet

##########################################
### Row & Column MultiIndex
##########################################

st.header("3. Measures by Client, Year, Quarter")


def first_quantile(series):
    return np.percentile(series, 25)


pivot = pd.pivot_table(
    df,
    index=["Client", "Year", "Quarter"],
    values=["Amount", "Tax"],
    aggfunc=["sum", "mean", "count", "std", first_quantile],
)
st.dataframe(pivot)

# Partial indexing/slicing: don't need to specify all levels
st.dataframe(
    pivot.loc[("Bridges Company", "2020", "Q1"), [("sum", "Amount"), ("mean", "Tax")]]
)
st.dataframe(pivot.loc[("Bridges Company"), "sum"])

# Slice range on both row / column
st.dataframe(
    pivot.loc[
        ("Bridges Company", "2019") : ("Chiral Corporation", "2022"), ["sum", "mean"]
    ]
)

# Select multiple rows/columns
st.dataframe(
    pivot.loc[
        [
            ("Bridges Company", "2020", "Q1"),
            ("Bridges Company", "2020", "Q2"),
            ("Chiral Corporation", "2020", "Q1"),
            ("Chiral Corporation", "2021", "Q1"),
        ],
        ["sum", "mean"],
    ]
)

# Cross-section for specific values (not shown in video)
st.dataframe(pivot.xs("Q1", level="Quarter", drop_level=False))
st.dataframe(
    pivot.xs(("Sol Company", "Q1"), level=("Client", "Quarter"), drop_level=False)
)

# Generic Slicing with IndexSlice
st.dataframe(
    pivot.loc[
        idx[
            pivot.index.get_level_values("Client").str.endswith("Corporation"),
            "2020",
            ["Q1", "Q4"],
        ],
        [("sum", "Amount"), ("first_quantile", "Tax")],
    ]
)

# Rows that paid more than 1M tax
st.dataframe(
    pivot.loc[
        (
            pivot[("sum", "Tax")] > 1_000_000,
            "2020",
            ["Q1", "Q4"],
        ),
        "sum",
    ]
)

# So many advanced use-cases, read the doc
# https://pandas.pydata.org/docs/user_guide/advanced.html#advanced-indexing-with-hierarchical-index

st.divider()

st.subheader("4. Plot")

st.dataframe(pivot)

r = pivot.stack()
r.index = r.index.set_names("Measure", level=-1)
r = r.reset_index()

st.dataframe(r)

fig = px.bar(
    r,
    x="Quarter",
    category_orders={"Quarter": ["Q1", "Q2", "Q3", "Q4"]},
    y="sum",
    color="Measure",
    barmode="group",
    facet_row="Client",
    facet_col="Year",
    facet_col_wrap=4,
)
st.plotly_chart(fig)

st.dataframe(pivot.loc[:, ("sum", "Amount")].unstack("Quarter"))
