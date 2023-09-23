from state.base import State
from state.models import User

import reflex as rx
import bcrypt

class AuthState(State):
    """The authentication state for sign up and login page."""

    username: str
    password: str
    confirm_password: str

    def signup(self):
        """Sign up a user."""
        with rx.session() as session:
            if self.password != self.confirm_password:
                return rx.window_alert("Passwords do not match.")
            if session.exec(User.select.where(User.username == self.username)).first():
                return rx.window_alert("Username already exists.")
            self.user = User(username=self.username,
                             password_hash=bcrypt.hashpw(bytes(self.password, 'utf-8'), bcrypt.gensalt()))
            session.add(self.user)
            session.expire_on_commit = False
            session.commit()
            return rx.redirect("/")

    def login(self):
        """Log in a user."""
        with rx.session() as session:
            user = session.exec(
                User.select.where(User.username == self.username)
            ).first()
            if user and bcrypt.checkpw(bytes(self.password, 'utf-8'), bytes(user.password_hash, 'utf-8') ):
                self.user = user
                return rx.redirect("/")
            else:
                return rx.window_alert("Invalid username or password.")