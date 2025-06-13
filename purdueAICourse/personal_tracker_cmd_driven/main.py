import json
from datetime import datetime
from typing import Dict, List, Optional
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

def display_menu() -> None:
    print("\n=== Personal Expense Tracker ===")
    print("1. Add new expense")
    print("2. View all expenses")
    print("3. Set monthly budget")
    print("4. View spending by category")
    print("5. View monthly summary")
    print("6. Save expenses")
    print("7. Load expenses")
    print("8. Exit")
    print("=============================")

def get_valid_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")

def main():
    tracker = ExpenseTracker()
    filename = "expenses.json"

    while True:
        display_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == "1":
            print("\nAvailable categories:", ", ".join(tracker.categories.keys()))
            category = input("Enter category: ").capitalize()
            if category not in tracker.categories:
                print("Invalid category. Using 'Other'.")
                category = "Other"
            
            amount = get_valid_float("Enter amount: $")
            description = input("Enter description: ")
            
            expense = Expense(amount, category, description)
            tracker.add_expense(expense)
            print("Expense added successfully!")

        elif choice == "2":
            if not tracker.expenses:
                print("\nNo expenses recorded yet.")
            else:
                print("\nAll Expenses:")
                for exp in tracker.expenses:
                    print(f"Date: {exp.date}, Category: {exp.category}, "
                          f"Amount: ${exp.amount:.2f}, Description: {exp.description}")

        elif choice == "3":
            print("\nAvailable categories:", ", ".join(tracker.categories.keys()))
            category = input("Enter category: ").capitalize()
            if category not in tracker.categories:
                print("Invalid category.")
                continue
            
            amount = get_valid_float("Enter monthly budget amount: $")
            tracker.set_monthly_budget(category, amount)
            print(f"Monthly budget for {category} set to ${amount:.2f}")

        elif choice == "4":
            print("\nSpending by Category:")
            for category, amount in tracker.categories.items():
                budget = tracker.monthly_budget.get(category, 0)
                print(f"{category}: ${amount:.2f}", end="")
                if budget > 0:
                    print(f" (Budget: ${budget:.2f}, Remaining: ${budget - amount:.2f})")
                else:
                    print()

        elif choice == "5":
            summary = tracker.get_monthly_summary()
            if not summary:
                print("\nNo expenses recorded yet.")
            else:
                print("\nMonthly Summary:")
                for month, data in summary.items():
                    print(f"\n{month}:")
                    print(f"Total Spending: ${data['total']:.2f}")
                    print("By Category:")
                    for category, amount in data['categories'].items():
                        print(f"  {category}: ${amount:.2f}")

        elif choice == "6":
            tracker.save_to_file(filename)
            print(f"\nExpenses saved to {filename}")

        elif choice == "7":
            tracker = ExpenseTracker.load_from_file(filename)
            print(f"\nExpenses loaded from {filename}")

        elif choice == "8":
            print("\nThank you for using the Personal Expense Tracker!")
            break

        else:
            print("\nInvalid choice. Please try again.")

if __name__ == "__main__":
    main()
