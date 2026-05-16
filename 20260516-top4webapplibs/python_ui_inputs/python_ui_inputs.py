################ <don't show> ################
import reflex as rx

from data import load_categories, sales_by_subcategory
################ </don't show> ###############


class State(rx.State):
    category: str = load_categories()[0]

    @rx.event
    def set_category(self, value: str):
        self.category = value

    @rx.var
    def chart_data(self) -> list[dict]:
        return sales_by_subcategory(self.category).to_dict("records")


def index() -> rx.Component:
    return rx.container(
        rx.vstack(
            rx.select(
                load_categories(),
                value=State.category,
                on_change=State.set_category,
                size="3",
                variant="soft",
                width="240px",
            ),
            rx.recharts.bar_chart(
                rx.recharts.bar(data_key="Sales"),
                rx.recharts.x_axis(data_key="Sub-Category"),
                rx.recharts.y_axis(),
                data=State.chart_data,
                width="100%",
                height=300,
            ),
            spacing="5",
            width="100%",
        ),
        size="1",
    )


################ <don't show> ################
app = rx.App()
app.add_page(index)
################ </don't show> ###############
