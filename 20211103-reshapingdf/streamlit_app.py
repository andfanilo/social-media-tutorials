import pandas as pd
import plotly.express as px
from statsmodels.multivariate.manova import MANOVA
import streamlit as st

df = pd.DataFrame(
    {
        "brand": ["After Ice", "Melting pot", "Yummy"],
        "France": [10, 12, 9],
        "USA": [7, 15, 12],
        "Japan": [6, 9, 19],
    }
)

df_long = df.melt(id_vars="brand", var_name="country", value_name="price")
df_wide = df_long.pivot(index="brand", columns="country", values="price").reset_index()

# Filter wide format
st.write(df_wide[
  (df_wide["France"]>10) & 
  (df_wide["USA"]>10)
])

# ANOVA on wide format
fit = MANOVA.from_formula("France + USA + Japan ~ brand", data=df_wide)
st.write(fit.mv_test())

# Plotly express grouped bar color by country on long format
fig = px.bar(df, x="brand", y="price", color="country")
st.plotly_chart(fig)
