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
            rx.button("Add", type_="submit", bg="white"),
        ),
        on_submit=State.add_item,
    )



def index() -> rx.Component:
    return rx.box(
        rx.heading("Budget for you week!", font_size = '2em'),
        rx.editable(
            rx.editable_preview(),
            rx.editable_input(),
            placeholder="0",
            on_submit=State.set_budget_target,
            font_size="2.25em",
            font_weight="bold"
        ),
        rx.heading("Spent"),
        rx.heading(State.total_spent),
        rx.heading("Remaining:"),
        rx.heading(State.total_remaining),
        rx.heading("Expenses List"),
        rx.unordered_list(
            rx.foreach(State.expense_items, lambda item: expense_item(item))
        ),
        new_item(),
        )


# Add state and page to the app.
app = rx.App()
app.add_page(index)
app.compile()
