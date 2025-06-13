from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import json
import os
from models import Expense, ExpenseTracker

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Initialize the expense tracker
tracker = ExpenseTracker()
DATA_FILE = "expenses.json"

# Load existing data if available
if os.path.exists(DATA_FILE):
    tracker = ExpenseTracker.load_from_file(DATA_FILE)

@app.route('/')
def index():
    return render_template('index.html', 
                         categories=tracker.categories.keys(),
                         expenses=tracker.expenses,
                         monthly_budget=tracker.monthly_budget)

@app.route('/add_expense', methods=['POST'])
def add_expense():
    try:
        amount = float(request.form['amount'])
        category = request.form['category']
        description = request.form['description']
        date = request.form.get('date') or datetime.now().strftime("%Y-%m-%d")

        if category not in tracker.categories:
            category = "Other"

        expense = Expense(amount, category, description, date)
        tracker.add_expense(expense)
        tracker.save_to_file(DATA_FILE)
        flash('Expense added successfully!', 'success')
    except ValueError:
        flash('Invalid amount entered!', 'error')
    except Exception as e:
        flash(f'Error adding expense: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    try:
        category = request.form['category']
        amount = float(request.form['amount'])
        
        if category in tracker.categories:
            tracker.set_monthly_budget(category, amount)
            tracker.save_to_file(DATA_FILE)
            flash(f'Budget for {category} set successfully!', 'success')
        else:
            flash('Invalid category!', 'error')
    except ValueError:
        flash('Invalid amount entered!', 'error')
    except Exception as e:
        flash(f'Error setting budget: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/get_summary')
def get_summary():
    summary = tracker.get_monthly_summary()
    category_spending = {
        category: tracker.get_category_spending(category)
        for category in tracker.categories
    }
    return jsonify({
        'monthly_summary': summary,
        'category_spending': category_spending,
        'total_spending': tracker.get_total_spending()
    })

@app.route('/delete_expense/<int:index>', methods=['POST'])
def delete_expense(index):
    try:
        if 0 <= index < len(tracker.expenses):
            del tracker.expenses[index]
            # Recalculate category totals
            tracker.categories = {cat: 0.0 for cat in tracker.categories}
            for exp in tracker.expenses:
                tracker.categories[exp.category] += exp.amount
            tracker.save_to_file(DATA_FILE)
            flash('Expense deleted successfully!', 'success')
        else:
            flash('Invalid expense index!', 'error')
    except Exception as e:
        flash(f'Error deleting expense: {str(e)}', 'error')
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True) 