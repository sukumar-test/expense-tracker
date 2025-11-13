"""Personal Expense Tracker Web Application.

This Flask application provides a web interface for tracking personal expenses.
It allows users to add, edit, delete, and view expenses, as well as analyze
expenses by category. The application uses SQLAlchemy for database operations
and provides both web UI and REST API endpoints.

Features:
    - Add new expenses with title, amount, category, date, and description
    - Edit existing expenses
    - Delete expenses
    - View all expenses sorted by date
    - View expenses grouped by category
    - REST API endpoint for retrieving expenses in JSON format

Database:
    SQLite database (expenses.db) with a single Expense table

Routes:
    / : Home page displaying all expenses
    /add : Add new expense
    /edit/<id> : Edit existing expense
    /delete/<id> : Delete expense
    /categories : View expenses grouped by category
    /api/expenses : REST API endpoint for expenses
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
    """SQLAlchemy model representing an expense entry.

    This model stores information about individual expenses including
    title, amount, category, date, and optional description.

    Attributes:
        id (int): Primary key identifier for the expense.
        title (str): Brief title or name of the expense (max 100 chars).
        amount (float): Monetary amount of the expense.
        category (str): Category classification (max 50 chars).
        date (datetime.date): Date when the expense occurred, defaults to current UTC date.
        description (str): Optional detailed description of the expense.
    """
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self):
        """Return string representation of the Expense object.

        Returns:
            str: String representation in format '<Expense {title}>'.
        """
        return f'<Expense {self.title}>'

# Routes
@app.route('/')
def index():
    """Display the home page with all expenses.

    Retrieves all expenses from the database ordered by date (newest first)
    and calculates the total amount. Renders the main index page.

    Returns:
        str: Rendered HTML template with expenses list and total amount.
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new expense to the database.

    Handles both GET and POST requests. On GET, displays the form for adding
    a new expense. On POST, validates and saves the expense data to the database.

    Form Parameters (POST):
        title (str): Title of the expense.
        amount (str): Amount of the expense (converted to float).
        category (str): Category classification for the expense.
        date (str): Date in 'YYYY-MM-DD' format, defaults to current date if not provided.
        description (str): Optional description of the expense.

    Returns:
        For GET: Rendered HTML template with the add expense form.
        For POST: Redirect to the index page after successful addition.

    Flashes:
        success: Message confirming expense was added successfully.
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

    Handles both GET and POST requests. On GET, displays the form pre-filled
    with the current expense data. On POST, updates the expense with new data.

    Args:
        id (int): The unique identifier of the expense to edit.

    Form Parameters (POST):
        title (str): Updated title of the expense.
        amount (str): Updated amount (converted to float).
        category (str): Updated category classification.
        date (str): Updated date in 'YYYY-MM-DD' format, keeps existing if not provided.
        description (str): Updated description.

    Returns:
        For GET: Rendered HTML template with the edit expense form.
        For POST: Redirect to the index page after successful update.

    Raises:
        404: If expense with the given id does not exist.

    Flashes:
        success: Message confirming expense was updated successfully.
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

    Retrieves the expense by id and permanently removes it from the database.

    Args:
        id (int): The unique identifier of the expense to delete.

    Returns:
        Redirect to the index page after successful deletion.

    Raises:
        404: If expense with the given id does not exist.

    Flashes:
        danger: Message confirming expense was deleted successfully.
    """
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    """Display expenses grouped and summed by category.

    Retrieves all expenses from the database and aggregates them by category,
    calculating the total amount spent in each category.

    Returns:
        str: Rendered HTML template with categories dictionary containing
            category names as keys and total amounts as values.
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
    """REST API endpoint to retrieve all expenses as JSON.

    Retrieves all expenses from the database ordered by date (newest first)
    and returns them as a JSON array. Each expense is serialized to include
    all fields with the date formatted as a string.

    Returns:
        Response: JSON response containing a list of expense dictionaries.
            Each dictionary contains:
                - id (int): Expense identifier
                - title (str): Expense title
                - amount (float): Expense amount
                - category (str): Expense category
                - date (str): Date in 'YYYY-MM-DD' format
                - description (str): Expense description
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
