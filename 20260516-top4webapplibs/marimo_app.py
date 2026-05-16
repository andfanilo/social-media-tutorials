import marimo

__generated_with = "0.23.6"
app = marimo.App()


@app.cell(hide_code=True)
def _():
    import altair as alt
    import marimo as mo

    from data import load_categories, sales_by_subcategory

    return alt, load_categories, mo, sales_by_subcategory


@app.cell
def _(load_categories, mo):
    category = mo.ui.dropdown(
        load_categories(),
        value=load_categories()[0],
        label="**Category**",
        full_width=True,
    )
    category
    return (category,)


@app.cell
def _(alt, category, sales_by_subcategory):
    alt.Chart(
        sales_by_subcategory(category.value)
    ).mark_bar().encode(
        x="Sub-Category:N", 
        y="Sales:Q"
    ).properties(width="container")
    return


if __name__ == "__main__":
    app.run()
