"""Expense Tracker Web Application.

This module implements a Flask-based web application for tracking personal expenses.
It provides functionality to add, edit, delete, and view expenses, as well as 
categorize them and view summaries by category.

The application uses SQLite as the database and SQLAlchemy as the ORM.

Attributes:
    app (Flask): The Flask application instance.
    db (SQLAlchemy): The SQLAlchemy database instance.
    
Example:
    To run the application::
    
        $ python app.py
        
    Or using the run script::
    
        $ ./run.sh
"""

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'expense_tracker_secret_key'

# Configure database
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'expenses.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define Expense model
class Expense(db.Model):
    """Database model representing an expense entry.
    
    This model stores information about individual expenses including their title,
    amount, category, date, and optional description.
    
    Attributes:
        id (int): Primary key, auto-incremented unique identifier for the expense.
        title (str): Title or name of the expense (max 100 characters).
        amount (float): Amount of the expense in currency units.
        category (str): Category of the expense (max 50 characters), e.g., 'Food', 'Utilities'.
        date (datetime.date): Date when the expense occurred. Defaults to current UTC date.
        description (str): Optional detailed description of the expense.
        
    Example:
        >>> expense = Expense(
        ...     title='Grocery Shopping',
        ...     amount=150.75,
        ...     category='Food',
        ...     date=datetime.now(),
        ...     description='Weekly groceries'
        ... )
        >>> db.session.add(expense)
        >>> db.session.commit()
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self):
        """Return a string representation of the Expense object.
        
        Returns:
            str: A string in the format '<Expense {title}>'.
            
        Example:
            >>> expense = Expense(title='Coffee')
            >>> repr(expense)
            '<Expense Coffee>'
        """
        return f'<Expense {self.title}>'

# Routes
@app.route('/')
def index():
    """Display the main index page with all expenses.
    
    This route fetches all expenses from the database, orders them by date
    (most recent first), calculates the total amount, and renders the index page.
    
    Returns:
        str: Rendered HTML template of the index page with expenses and total amount.
        
    Template Variables:
        expenses (list): List of all Expense objects ordered by date descending.
        total_amount (float): Sum of all expense amounts.
        
    Example:
        GET / returns the main page with all expenses listed.
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new expense to the database.
    
    For GET requests, displays the form to add a new expense.
    For POST requests, validates and saves the new expense to the database.
    
    Returns:
        str: For GET requests, rendered add expense form template.
             For POST requests, redirects to index page after successful addition.
             
    Form Data (POST):
        title (str): Title of the expense (required).
        amount (float): Amount of the expense (required).
        category (str): Category of the expense (required).
        date (str): Date in YYYY-MM-DD format (optional, defaults to current date).
        description (str): Optional description of the expense.
        
    Flash Messages:
        On success: 'Expense added successfully!' with category 'success'.
        
    Example:
        POST /add with form data creates a new expense and redirects to /.
        GET /add displays the add expense form.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        amount = float(request.form.get('amount'))
        category = request.form.get('category')
        date_str = request.form.get('date')
        description = request.form.get('description')
        
        date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
        
        expense = Expense(
            title=title, 
            amount=amount, 
            category=category, 
            date=date, 
            description=description
        )
        
        db.session.add(expense)
        db.session.commit()
        
        flash('Expense added successfully!', 'success')
        return redirect(url_for('index'))
    
    # Pass today's date to the template
    return render_template('add.html', now=datetime.utcnow())

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit an existing expense.
    
    For GET requests, displays the form to edit an expense with pre-filled data.
    For POST requests, updates the expense with new data.
    
    Args:
        id (int): The unique identifier of the expense to edit.
        
    Returns:
        str: For GET requests, rendered edit expense form template.
             For POST requests, redirects to index page after successful update.
             
    Raises:
        404: If the expense with the given ID does not exist.
        
    Form Data (POST):
        title (str): Updated title of the expense (required).
        amount (float): Updated amount of the expense (required).
        category (str): Updated category of the expense (required).
        date (str): Updated date in YYYY-MM-DD format (optional).
        description (str): Updated description of the expense.
        
    Flash Messages:
        On success: 'Expense updated successfully!' with category 'success'.
        
    Example:
        POST /edit/1 with form data updates expense with ID 1 and redirects to /.
        GET /edit/1 displays the edit form for expense with ID 1.
    """
    expense = Expense.query.get_or_404(id)
    
    if request.method == 'POST':
        expense.title = request.form.get('title')
        expense.amount = float(request.form.get('amount'))
        expense.category = request.form.get('category')
        date_str = request.form.get('date')
        expense.date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else expense.date
        expense.description = request.form.get('description')
        
        db.session.commit()
        flash('Expense updated successfully!', 'success')
        return redirect(url_for('index'))
        
    return render_template('edit.html', expense=expense)

@app.route('/delete/<int:id>')
def delete(id):
    """Delete an expense from the database.
    
    Removes the expense with the specified ID from the database and redirects
    to the index page.
    
    Args:
        id (int): The unique identifier of the expense to delete.
        
    Returns:
        Response: Redirects to the index page after deletion.
        
    Raises:
        404: If the expense with the given ID does not exist.
        
    Flash Messages:
        On success: 'Expense deleted successfully!' with category 'danger'.
        
    Example:
        GET /delete/1 deletes expense with ID 1 and redirects to /.
    """
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    """Display expenses grouped and summed by category.
    
    Fetches all expenses and calculates the total amount spent per category,
    then renders a summary page showing category-wise spending.
    
    Returns:
        str: Rendered HTML template showing categories and their total amounts.
        
    Template Variables:
        categories (dict): Dictionary mapping category names (str) to total amounts (float).
                          Example: {'Food': 250.50, 'Utilities': 150.00}
                          
    Example:
        GET /categories returns a page showing expense totals grouped by category.
    """
    expenses = Expense.query.all()
    categories = {}
    
    for expense in expenses:
        if expense.category in categories:
            categories[expense.category] += expense.amount
        else:
            categories[expense.category] = expense.amount
            
    return render_template('categories.html', categories=categories)

@app.route('/api/expenses')
def api_expenses():
    """API endpoint to retrieve all expenses in JSON format.
    
    Returns all expenses from the database as a JSON array, ordered by date
    (most recent first). This endpoint can be used for programmatic access
    to expense data.
    
    Returns:
        Response: JSON array of expense objects, each containing:
            - id (int): Unique identifier of the expense
            - title (str): Title of the expense
            - amount (float): Amount of the expense
            - category (str): Category of the expense
            - date (str): Date in YYYY-MM-DD format
            - description (str): Description of the expense (may be null)
            
    Example:
        GET /api/expenses returns:
        [
            {
                "id": 1,
                "title": "Grocery Shopping",
                "amount": 150.75,
                "category": "Food",
                "date": "2025-05-01",
                "description": "Weekly groceries"
            },
            ...
        ]
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    result = []
    
    for expense in expenses:
        result.append({
            'id': expense.id,
            'title': expense.title,
            'amount': expense.amount,
            'category': expense.category,
            'date': expense.date.strftime('%Y-%m-%d'),
            'description': expense.description
        })
        
    return jsonify(result)

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
