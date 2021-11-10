import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

penguins = sns.load_dataset("penguins")
st.dataframe(penguins[["species", "flipper_length_mm"]].sample(6))

# Slide 2 - state-machine pyplot
f = plt.figure(figsize=(9, 7))
sns.histplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
plt.title("Hello Penguins!")
st.pyplot(f)

plt.figure(figsize=(6, 6))
sns.kdeplot(data=penguins, x="flipper_length_mm", hue="species", multiple="stack")
plt.title("Hello again!")
st.pyplot(plt.gcf())

# Slide 3 - Object Oriented
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
st.pyplot(fig)
