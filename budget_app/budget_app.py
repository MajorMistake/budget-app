"""Welcome to Reflex! This file outlines the steps to create a basic app."""
from rxconfig import config
from typing import Optional, List, Dict
from sqlmodel import Field

import reflex as rx


class Expense_Item(rx.Model, table=True):
    expense_id: int = Field(primary_key=True)
    expense_name: str = Field()
    expense_amount: float = Field()



class State(rx.State):
    budget_target: float
    spent: float
    expense_items: Dict[str, float] = {}


    @rx.var
    def total_spent(self):
        return round(sum(self.expense_items.values()), 2)

    @rx.var
    def total_remaining(self):
        return round(self.budget_target - self.total_spent, 2)
    
    @rx.var
    def spent_percentage(self) -> float:
        if self.budget_target == 0:
            return 0
        else:
            return round(self.total_spent/self.budget_target, 1)*100
        
    @rx.var
    def spent_bar_color(self):
        if self.spent_percentage < 80:
            return "green"
        elif self.spent_percentage < 90:
            return "yellow"
        else:
            return "red"


    def add_item(self, form_data: dict[str, str]):
        name, amount = form_data["expense_name"], float(form_data["expense_amount"])
        self.expense_items[name] = amount
        return [
            rx.set_value(field_id, "")
            for field_id in form_data
        ]
    
    def delete_item(self, item: List):
        del self.expense_items[item[0]]


def expense_item(item: rx.Var[List]) -> rx.Component:
    """Render an item in the expense list.

    NOTE: When using `rx.foreach`, the item will be a Var[str] rather than a str.

    Args:
        item: The todo list item.

    Returns:
        A single rendered todo list item.
    """
    return rx.list_item(
        rx.hstack(
            # The item text.
            rx.text(item[0], font_size="1.25em"),
            rx.text(item[1], font_size="1.25em"),
            # A button to finish the item.
            rx.button(
                on_click=lambda: State.delete_item(item),
                height="1.5em",
                background_color="white",
                border="1px solid red",
            ),
        )
    )

def new_item() -> rx.Component:
    """Render the new item form.

    See: https://reflex.dev/docs/library/forms/form

    Returns:
        A form to add a new item to the todo list.
    """
    return rx.form(
        # Pressing enter will submit the form.
        rx.hstack(
            rx.input(
                id="expense_name",
                placeholder="Add an expense...",
            ),
            rx.input(
                id="expense_amount",
                placeholder="Expense Amount"
            ),
        ),
        # Clicking the button will also submit the form.
        rx.center(
            rx.button("Add", type_="submit", bg="white", margin_top='.5em'),
        ),
        on_submit=State.add_item,
    )



def index() -> rx.Component:
    return rx.container(
        rx.heading("Budget for you week!", font_size = '2em'),
        rx.divider(border_color="black", margin="1em 0em"),
        rx.cond(
            State.spent_bar_color == "red",
            rx.progress(value=State.spent_percentage, width="100%", color_scheme="red"),
            ),
        rx.cond(
            State.spent_bar_color == "yellow",
            rx.progress(value=State.spent_percentage, width="100%", color_scheme="yellow"),
            ),
        rx.cond(
            State.spent_bar_color == "green",
            rx.progress(value=State.spent_percentage, width="100%", color_scheme="green"),
            ),
        rx.hstack(
            rx.hstack(
                rx.text("Spending Limit:"),
                rx.editable(
                    rx.editable_preview(),
                    rx.editable_input(),
                    placeholder="Enter Limit",
                    on_submit=State.set_budget_target,
                    font_size="1em",
                    border="1px solid gray",
                    border_radius=".75em",
                    padding=".25em"
                ),
            ),
            rx.hstack(
                rx.text("Total Spent:"),
                rx.text(State.total_spent),
            ),
            rx.hstack(
                rx.text("Remaining:"),
                rx.text(State.total_remaining),  
            ),
            margin_top="1em"
        ),
        rx.divider(border_color="black", margin="1em 0em"),
        rx.heading("Expenses List", size='lg', margin_bottom='.5em'),
        rx.unordered_list(
            rx.foreach(State.expense_items, lambda item: expense_item(item)),
            list_style_type="none"
        ),
        new_item(),
        background_color="#EDEDED",
        padding="1em",
        margin_top="2em",
        border_radius=".5em",
        center_content=True,
        )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
