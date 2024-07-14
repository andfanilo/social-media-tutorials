import streamlit as st
import plotly.express as px
import seaborn as sns

st.title("Cool Dashboard")

df = sns.load_dataset("penguins")

fig = px.scatter(
    df, 
    x="bill_length_mm", 
    y="bill_depth_mm", 
    color="species",
)

st.plotly_chart(fig)