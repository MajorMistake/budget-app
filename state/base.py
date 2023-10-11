from typing import Optional
from state.models import User

import reflex as rx

class State(rx.State):
    """The base state for the app."""

    user: Optional[User] = None

    def logout(self):
        """Log out a user."""
        self.reset()
        return rx.redirect("/")

    @rx.var
    def logged_in(self):
        """Check if a user is logged in."""
        return self.user is not None