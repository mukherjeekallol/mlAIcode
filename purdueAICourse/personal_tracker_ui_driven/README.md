# Personal Expense Tracker

A modern web-based application for tracking personal expenses with an intuitive user interface and powerful visualization features.

## Overview

The Personal Expense Tracker is a Flask-based web application that helps users manage their daily expenses, set budgets, and track spending patterns. It provides a clean, responsive interface with real-time data visualization and persistent storage.

## Features

### Core Functionality
- Add and categorize daily expenses
- Set monthly budgets for different categories
- Track spending against budgets
- View spending patterns and trends
- Delete expenses
- Persistent data storage using JSON

### Categories
- Food
- Transportation
- Housing
- Entertainment
- Utilities
- Shopping
- Healthcare
- Other

### Visualizations
- Doughnut chart for category-wise spending distribution
- Line chart for monthly spending trends
- Summary cards showing total spending and monthly averages
- Budget progress indicators

## Technical Architecture

### Backend (Python/Flask)
- **Models** (`models.py`):
  - `Expense` class: Represents individual expenses with amount, category, description, and date
  - `ExpenseTracker` class: Manages expenses, budgets, and provides data analysis methods
  - JSON-based data persistence

- **Application** (`app.py`):
  - Flask web server
  - RESTful endpoints for CRUD operations
  - Data validation and error handling
  - Flash messages for user feedback

### Frontend
- **Templates** (`templates/`):
  - `base.html`: Base template with common styling and layout
  - `index.html`: Main application interface

- **Technologies**:
  - Bootstrap 5 for responsive design
  - Chart.js for data visualization
  - Font Awesome for icons
  - Custom CSS for enhanced styling

### Data Flow
1. User interactions trigger HTTP requests to Flask endpoints
2. Backend processes requests and updates the data model
3. Data is persisted to JSON file
4. Frontend receives updated data and refreshes visualizations
5. Real-time feedback provided through flash messages

## Project Structure
```
personal_tracker_ui_driven/
├── app.py              # Flask application and routes
├── models.py           # Data models and business logic
├── requirements.txt    # Python dependencies
├── expenses.json       # Data storage
└── templates/          # HTML templates
    ├── base.html       # Base template
    └── index.html      # Main application template
```

## Dependencies
- Flask 3.0.2
- Flask-WTF 1.2.1
- WTForms 3.1.2
- python-dateutil 2.8.2

## Setup and Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Unix/MacOS
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Access the application at `http://localhost:5000`

## Security Features
- Input validation for all forms
- CSRF protection through Flask-WTF
- Secure data storage
- Error handling and user feedback

## Future Enhancements
1. User authentication and multiple user support
2. Export functionality (CSV, PDF)
3. Advanced filtering and search
4. Custom category management
5. Receipt image upload and OCR
6. Email notifications for budget alerts
7. Mobile app integration

## Best Practices Implemented
- Separation of concerns (MVC pattern)
- Responsive design
- Real-time data updates
- Error handling
- Code modularity
- Clean and intuitive UI
- Persistent data storage
- Input validation
- Security measures

## Performance Considerations
- Efficient data loading and caching
- Optimized database queries
- Responsive UI with minimal page reloads
- Efficient chart rendering
- Proper error handling and recovery

## Contributing
Feel free to submit issues and enhancement requests! 