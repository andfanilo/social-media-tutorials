import reflex as rx

config = rx.Config(
    app_name="python_ui_inputs",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)