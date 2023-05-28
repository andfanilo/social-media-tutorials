import streamlit as st
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Bi Dashboard")

cols = st.columns(3)

df = px.data.iris()
df["e"] = df["sepal_width"]/100
cols[0].plotly_chart(px.scatter(df, x="sepal_width", y="sepal_length", color="species", error_x="e", error_y="e"))
cols[1].plotly_chart(px.scatter(df, x="sepal_length", y="sepal_width", marginal_x="histogram", marginal_y="rug"))

df = px.data.tips()
cols[2].plotly_chart(px.density_heatmap(df, x="total_bill", y="tip"))

cols = st.columns(4)

df = px.data.gapminder()

cols[0].plotly_chart(px.area(df, x="year", y="pop", color="continent", line_group="country"))

df = px.data.stocks()
cols[1].plotly_chart(px.line(df, x='date', y="GOOG"))

data = dict(
    number=[39, 27.4, 20.6, 11, 2],
    stage=["Website visit", "Downloads", "Potential customers", "Requested price", "invoice sent"]
)
cols[2].plotly_chart(px.funnel(data, x='number', y='stage'))

df = px.data.tips()
cols[3].plotly_chart(px.histogram(df, x="total_bill"))