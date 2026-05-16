################ <don't show> ################
from nicegui import ui

from data import load_categories, sales_by_subcategory

ui.add_head_html(
    "<style>.nicegui-content { max-width: 600px; margin: 0 auto; }</style>"
)


def chart_options(category: str) -> dict:
    df = sales_by_subcategory(category)
    return {
        "xAxis": {"type": "category", "data": df["Sub-Category"].tolist()},
        "yAxis": {"type": "value"},
        "series": [{"type": "bar", "data": df["Sales"].tolist()}],
    }


categories = load_categories()
initial = categories[0]


def on_change(e):
    df = sales_by_subcategory(e.value)
    chart.options["xAxis"]["data"] = df["Sub-Category"].tolist()
    chart.options["series"][0]["data"] = df["Sales"].tolist()
    chart.update()
################ </don't show> ###############

(
    ui.select(categories, value=initial, label="Category", on_change=on_change)
    .props("outlined")
    .classes("w-64 text-lg my-2")
)
chart = ui.echart(chart_options(initial))

################ <don't show> ################
ui.run()
################ </don't show> ###############
