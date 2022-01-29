import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

penguins = sns.load_dataset("penguins")
st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))

# Create Figure beforehand
fig = plt.figure(figsize=(9, 7))
sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
plt.title("Hello Penguins!")
st.pyplot(fig)

# Let Seaborn create the Figure
sns.kdeplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
plt.title("Hello again!")
st.pyplot(plt.gcf())

# Personally not a big fan of state based matplotlib
# Pre-existing axes for the plot. Otherwise, call matplotlib.pyplot.gca() internally.

# Methods that return a figure
fig = sns.pairplot(penguins, hue="species")
st.pyplot(fig)

# Methods that return Ax -> you will get AttributeError: 'AxesSubplot' object has no attribute 'savefig'
fig = sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm")
try:
    st.pyplot(fig)
except Exception as e:
    st.exception(e)

# Fix it
ax = sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm")
st.pyplot(ax.get_figure())

# Create ax and figure beforehand, most libs have this - object-oriented
fig, ax = plt.subplots()
sns.scatterplot(data=penguins, x="flipper_length_mm", y="bill_length_mm", ax=ax)
st.pyplot(fig)

# Create Figure with multiple axes
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6, 4))
sns.histplot(
    data=penguins, x="flipper_length_mm", hue="species", multiple="stack", ax=ax1
)
sns.kdeplot(
    data=penguins, x="flipper_length_mm", hue="species", multiple="stack", ax=ax2
)
ax1.set_title("Hello Penguins!")
ax2.set_title("Hello again!")
ax2.grid(True)

fig.set_tight_layout(True)
st.pyplot(fig)
