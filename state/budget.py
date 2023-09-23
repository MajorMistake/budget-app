from typing import Dict, List
from state.base import State

import reflex as rx

class BudgetState(State):
    budget_target: float
    spent: float
    expense_items: Dict[str, float] = {}
    buckets: Dict[str, float] = {}


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