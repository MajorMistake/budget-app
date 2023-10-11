from typing import Dict, List, Optional
from state.base import State
from state.models import User_Data

import reflex as rx
import json

class BudgetState(State):
    budget_target: float
    spent: float
    expense_items: Dict[str, float] = {}
    buckets: Dict[str, float] = {}

    db_record: Optional[User_Data] = None


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
        
    def login_user(self, form_data: dict[str, str]):
        pass


    def add_item(self, form_data: dict[str, str]):
        name, amount = form_data["expense_name"], float(form_data["expense_amount"])
        self.expense_items[name] = amount
        return [
            rx.set_value(field_id, "")
            for field_id in form_data
        ]
    
    def delete_item(self, item: List):
        del self.expense_items[item[0]]

    def add_bucket(self, form_data: dict[str, str]):
        name, amount = form_data["bucket_name"], float(form_data["bucket_amount"])
        self.buckets[name] = amount
        return [
            rx.set_value(field_id, "")
            for field_id in form_data
        ]
    
    def delete_bucket(self, bucket: List):
        del self.buckets[bucket[0]]

    def load_data(self):
        with rx.session() as session:
            self.db_record = session.exec(User_Data.select.where(User_Data.user_id == self.user.user_id)).first()
            self.budget_target = self.db_record.budget_target
            self.expense_items = json.loads(self.db_record.transactions)
            self.buckets = json.loads(self.db_record.buckets)

    def save_data(self):
        with rx.session() as session:
            if session.exec(User_Data.select.where(User_Data.user_id == self.user.user_id)).first():
                self.db_record.budget_target = self.budget_target
                self.db_record.transactions = json.dumps(self.expense_items)
                self.db_record.buckets = json.dumps(self.buckets)
                session.add(self.db_record)
                session.commit()
            else:
                session.add(User_Data(user_id=self.user.user_id ,budget_target=self.budget_target, transactions=json.dumps(self.expense_items),
                                    buckets=json.dumps(self.buckets)))
                session.commit()

    def clear_data(self):
        self.reset()

    def check_login(self):
        """Check if a user is logged in."""
        if not self.logged_in:
            return rx.redirect("/login")
        else:
            self.load_data()