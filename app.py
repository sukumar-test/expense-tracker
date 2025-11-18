"""Expense Tracker Flask Application.

This module implements a web-based expense tracking system using Flask and SQLAlchemy.
It provides functionality to add, edit, delete, and categorize expenses, as well as
view expense summaries and access data through a REST API.
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
    """Database model for storing expense records.

    This class represents an expense entry in the database with all necessary
    attributes for tracking personal or business expenses.

    Attributes:
        id (int): Primary key for the expense record.
        title (str): Short title or name of the expense (max 100 characters).
        amount (float): Monetary amount of the expense.
        category (str): Category classification for the expense (max 50 characters).
        date (datetime.date): Date when the expense occurred (defaults to current UTC time).
        description (str): Optional detailed description of the expense.
    """

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self):
        return f'<Expense {self.title}>'

# Routes
@app.route('/')
def index():
    """Display the main dashboard with all expenses.

    This route retrieves all expenses from the database, sorts them by date
    in descending order, calculates the total amount, and renders the main
    index page.

    Returns:
        str: Rendered HTML template displaying all expenses and total amount.
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new expense to the database.

    Handles both GET and POST requests. On GET, displays the form for adding
    a new expense. On POST, validates and saves the new expense to the database.

    Returns:
        str: On GET, renders the add expense form. On POST success, redirects
        to the index page after adding the expense and displaying a flash message.

    Note:
        If no date is provided in the form, the current UTC time is used.
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
    """Edit an existing expense in the database.

    Handles both GET and POST requests. On GET, displays the form pre-filled
    with the expense's current data. On POST, updates the expense with new values.

    Args:
        id (int): The unique identifier of the expense to edit.

    Returns:
        str: On GET, renders the edit form with current expense data. On POST
        success, redirects to the index page after updating the expense and
        displaying a flash message.

    Raises:
        404: If no expense with the given id exists in the database.
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

    Removes the specified expense from the database and redirects to the
    main page with a confirmation message.

    Args:
        id (int): The unique identifier of the expense to delete.

    Returns:
        werkzeug.wrappers.Response: Redirect to the index page after deletion.

    Raises:
        404: If no expense with the given id exists in the database.
    """
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    """Display expenses grouped and summarized by category.

    Retrieves all expenses from the database and aggregates them by category,
    calculating the total amount spent per category.

    Returns:
        str: Rendered HTML template displaying categories with their
        corresponding total amounts.
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

    Returns all expenses from the database in JSON format, sorted by date
    in descending order. Useful for external integrations or AJAX requests.

    Returns:
        flask.Response: JSON response containing a list of expense objects.
        Each expense object includes: id, title, amount, category, date
        (formatted as 'YYYY-MM-DD'), and description.
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
