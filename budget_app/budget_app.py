import reflex as rx

from pages.home import index
from pages.login import login
from pages.signup import signup
from state.base import State

# Add state and page to the app.
app = rx.App()
app.add_page(index, on_load=State.check_login)
app.add_page(login)
app.add_page(signup)
app.compile()
