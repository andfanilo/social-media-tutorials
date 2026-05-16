################ <don't show> ################
import streamlit as st

from data import load_categories, sales_by_subcategory
################ </don't show> ###############

category = st.selectbox(
    "Category", 
    load_categories(),
)

st.bar_chart(
    sales_by_subcategory(category), 
    x="Sub-Category", 
    y="Sales",
)
