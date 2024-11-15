import marimo

__generated_with = "0.9.17"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import plotly.express as px
    return mo, px


@app.cell
def __(mo):
    mo.md(
        r"""
        # Hello DataFans

        This is my app
        """
    )
    return


@app.cell
def __(mo):
    _df = mo.sql(
        f"""
        attach 'data/needful_things.duckdb' AS needful_things
        """
    )
    return (needful_things,)


@app.cell
def __(all_categories, mo):
    dropdown = mo.ui.dropdown(
        dict(zip(all_categories["category_key"], all_categories["category_value"])), 
        label="Select Category", 
        value="All Categories", 
        allow_select_none=False
    )
    dropdown
    return (dropdown,)


@app.cell
def __(mo, needful_things, orders):
    orders = mo.sql(
        f"""
        select * from needful_things.orders
        """, output=False
    )
    return (orders,)


@app.cell
def __(mo, needful_things, orders):
    all_categories = mo.sql(
        f"""
        select 'All Categories' as category_key, '%' as category_value
        union all
        select
             category , category 
        from needful_things.orders
        group by category
        """, output=False
    )
    return (all_categories,)


@app.cell
def __(mo, orders_by_category, px):
    _plot = px.area(orders_by_category, x="month", y="sales_usd", color="category")
    mo.ui.plotly(_plot)
    return


@app.cell
def __(dropdown, mo, needful_things, orders):
    orders_by_category = mo.sql(
        f"""
        select
          date_trunc('month', order_datetime) as month,
          sum(sales) as sales_usd,
          category
        from needful_things.orders
        where category like '{dropdown.value}'
        group by all
        order by sales_usd desc
        """
    )
    return (orders_by_category,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
