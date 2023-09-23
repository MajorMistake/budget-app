from sqlmodel import Field

import reflex as rx


class User_Data(rx.Model, table=True):
    user_id: int = Field(primary_key=True)
    budget_target: float = Field()
    transactions: str = Field()
    buckets: str = Field()


class User(rx.Model, table=True):
    user_id: int = Field(primary_key=True)
    username: str = Field()
    password_hash: str = Field()
