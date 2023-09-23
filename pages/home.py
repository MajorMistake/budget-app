from typing import List
from state.budget import BudgetState

import reflex as rx

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
                on_click=lambda: BudgetState.delete_item(item),
                height="1.5em",
                background_color="white",
                border="1px solid red",
            ),
        )
    )

def new_item() -> rx.Component:
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
        on_submit=BudgetState.add_item,
    )

def money_bucket(bucket: rx.Var[List]) -> rx.Component:
    return rx.hstack(
        rx.text(bucket[0]),
        rx.text(bucket[1]),
        rx.button(
                on_click=lambda: BudgetState.delete_bucket(bucket),
                height="1.5em",
                background_color="white",
                border="1px solid red",
            ),
    )

def new_bucket() -> rx.Component:
    return rx.form(
        # Pressing enter will submit the form.
        rx.hstack(
            rx.input(
                id="bucket_name",
                placeholder="Bucket Name",
            ),
            rx.input(
                id="bucket_amount",
                placeholder="Bucket Amount"
            ),
        ),
        # Clicking the button will also submit the form.
        rx.center(
            rx.button("Add", type_="submit", bg="white", margin_top='.5em'),
        ),
        on_submit=BudgetState.add_bucket,
    )

def login_form() -> rx.Component:
    return rx.form(
        rx.input(id="username", placeholder="Username"),
        rx.input(id="password", placeholder="Password", type_="password"),
        rx.button("Login", type_="submit", bg="white", margin_top='.5em'),
    )


def index() -> rx.Component:
    return rx.container(
        rx.heading("Budget for you week!", font_size = '2em'),
        rx.divider(border_color="black", margin="1em 0em"),
        rx.cond(
            BudgetState.spent_bar_color == "red",
            rx.progress(value=BudgetState.spent_percentage, width="100%", color_scheme="red"),
            ),
        rx.cond(
            BudgetState.spent_bar_color == "yellow",
            rx.progress(value=BudgetState.spent_percentage, width="100%", color_scheme="yellow"),
            ),
        rx.cond(
            BudgetState.spent_bar_color == "green",
            rx.progress(value=BudgetState.spent_percentage, width="100%", color_scheme="green"),
            ),
        rx.hstack(
            rx.hstack(
                rx.text("Spending Limit:"),
                rx.editable(
                    rx.editable_preview(),
                    rx.editable_input(),
                    placeholder="Enter Limit",
                    on_submit=BudgetState.set_budget_target,
                    font_size="1em",
                    border="1px solid gray",
                    border_radius=".75em",
                    padding=".25em"
                ),
            ),
            rx.hstack(
                rx.text("Total Spent:"),
                rx.text(BudgetState.total_spent),
            ),
            rx.hstack(
                rx.text("Remaining:"),
                rx.text(BudgetState.total_remaining),  
            ),
            margin_top="1em"
        ),
        rx.divider(border_color="black", margin="1em 0em"),
        rx.heading("Buckets"),
        rx.list(
            rx.foreach(BudgetState.buckets, lambda bucket: money_bucket(bucket))
        ),
        new_bucket(),
        rx.divider(border_color="black", margin="1em 0em"),
        rx.heading("Expenses List", size='lg', margin_bottom='.5em'),
        rx.unordered_list(
            rx.foreach(BudgetState.expense_items, lambda item: expense_item(item)),
            list_style_type="none"
        ),
        new_item(),
        background_color="#EDEDED",
        padding="1em",
        margin_top="2em",
        border_radius=".5em",
        center_content=True,
        )