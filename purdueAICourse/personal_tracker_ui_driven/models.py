from datetime import datetime
from typing import Dict, List, Optional
import json
import os

class Expense:
    def __init__(self, amount: float, category: str, description: str, date: str = None):
        self.amount = amount
        self.category = category
        self.description = description
        self.date = date or datetime.now().strftime("%Y-%m-%d")

    def to_dict(self) -> Dict:
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description,
            "date": self.date
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Expense':
        return cls(
            amount=data["amount"],
            category=data["category"],
            description=data["description"],
            date=data["date"]
        )

class ExpenseTracker:
    def __init__(self):
        self.expenses: List[Expense] = []
        self.monthly_budget: Dict[str, float] = {}
        self.categories = {
            "Food": 0.0,
            "Transportation": 0.0,
            "Housing": 0.0,
            "Entertainment": 0.0,
            "Utilities": 0.0,
            "Shopping": 0.0,
            "Healthcare": 0.0,
            "Other": 0.0
        }

    def add_expense(self, expense: Expense) -> None:
        self.expenses.append(expense)
        self.categories[expense.category] += expense.amount

    def set_monthly_budget(self, category: str, amount: float) -> None:
        self.monthly_budget[category] = amount

    def get_category_spending(self, category: str) -> float:
        return sum(exp.amount for exp in self.expenses if exp.category == category)

    def get_total_spending(self) -> float:
        return sum(exp.amount for exp in self.expenses)

    def get_monthly_summary(self) -> Dict[str, Dict[str, float]]:
        summary = {}
        for expense in self.expenses:
            month = expense.date[:7]  # Get YYYY-MM
            if month not in summary:
                summary[month] = {"total": 0.0, "categories": {}}
            
            summary[month]["total"] += expense.amount
            if expense.category not in summary[month]["categories"]:
                summary[month]["categories"][expense.category] = 0.0
            summary[month]["categories"][expense.category] += expense.amount
        
        return summary

    def save_to_file(self, filename: str) -> None:
        data = {
            "expenses": [exp.to_dict() for exp in self.expenses],
            "monthly_budget": self.monthly_budget,
            "categories": self.categories
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)

    @classmethod
    def load_from_file(cls, filename: str) -> 'ExpenseTracker':
        tracker = cls()
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                data = json.load(f)
                tracker.expenses = [Expense.from_dict(exp) for exp in data["expenses"]]
                tracker.monthly_budget = data["monthly_budget"]
                tracker.categories = data["categories"]
        return tracker 