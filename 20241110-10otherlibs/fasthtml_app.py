# type: ignore
import duckdb
import plotly.express as px
from fasthtml.common import *

tailwind = Script(src="https://cdn.tailwindcss.com")
daisyui = Link(
    rel="stylesheet",
    href="https://cdn.jsdelivr.net/npm/daisyui@4.12.14/dist/full.min.css",
)
plotlyjs = Script(src="https://cdn.plot.ly/plotly-2.35.2.min.js")

app, rt = fast_app(
    live=True,
    pico=False,
    hdrs=(tailwind, daisyui, plotlyjs),
)


def get_categories():
    with duckdb.connect("data/needful_things.duckdb") as connection:
        categories = connection.sql(
            "select distinct(category) from orders order by category"
        ).fetchall()
    return [c[0] for c in categories]


@app.get("/plot")
def plot_sum_data(filter_category: str = "%"):
    with duckdb.connect("data/needful_things.duckdb") as connection:
        data = connection.sql(f"""
            select
                date_trunc('month', order_datetime) as month,
                sum(sales) as sales_usd,
                category
            from orders
            where category like '{filter_category}'
            group by all
            order by sales_usd desc
        """).df()
    fig = px.bar(data, x="month", y="sales_usd", color="category")
    fig_dict = fig.to_json()
    plot_js = Script(f"var data = {fig_dict}; Plotly.react('plotly-chart', data);")
    return plot_js


@app.get("/")
def home():
    return Div(
        H1("Hello DataFans", cls="text-4xl font-bold"),
        P("Select a category", cls="text-lg pt-4"),
        Select(
            Option("---", value="%"),
            *[Option(category, value=category) for category in get_categories()],
            name="filter_category",
            hx_get="/plot",
            hx_trigger="load,change",
            hx_target="#plotly-script",
            cls="mt-4 select select-bordered",
        ),
        Div(id="plotly-chart", cls="mt-4"),
        Div(id="plotly-script"),
        cls="mt-4 px-8",
    )


serve()
