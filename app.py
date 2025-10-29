"""
Expense Tracker Application

A Flask-based web application for tracking personal expenses. This application allows users to:
- Add, edit, and delete expenses
- Categorize expenses
- View expense summaries and visualizations
- Track expenses over time

The application uses SQLAlchemy with SQLite for data persistence and Bootstrap for the UI.

Author: Expense Tracker Team
License: MIT
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
    """
    SQLAlchemy model representing an expense entry.
    
    Attributes:
        id (int): Primary key, auto-incremented unique identifier
        title (str): Short title or name of the expense (max 100 characters)
        amount (float): Cost of the expense in decimal format
        category (str): Category classification (max 50 characters)
        date (date): Date when the expense occurred (defaults to current UTC date)
        description (str): Optional detailed description of the expense
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)

    def __repr__(self):
        """
        String representation of the Expense object.
        
        Returns:
            str: A string representation showing the expense title
        """
        return f'<Expense {self.title}>'

# Routes
@app.route('/')
def index():
    """
    Render the home page with a list of all expenses.
    
    Retrieves all expenses from the database ordered by date (newest first)
    and calculates the total amount spent across all expenses.
    
    Returns:
        str: Rendered HTML template for the index page with expense list and total
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """
    Handle adding a new expense.
    
    GET: Display the form for adding a new expense
    POST: Process the submitted form data and create a new expense record
    
    Form fields:
        - title (str): Name of the expense
        - amount (float): Cost of the expense
        - category (str): Expense category
        - date (str): Date in YYYY-MM-DD format
        - description (str): Optional description
    
    Returns:
        GET: Rendered HTML template for the add expense form
        POST: Redirect to index page on success with flash message
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
    """
    Handle editing an existing expense.
    
    GET: Display the form for editing an expense with pre-filled data
    POST: Process the submitted form data and update the expense record
    
    Args:
        id (int): The unique identifier of the expense to edit
    
    Form fields:
        - title (str): Updated name of the expense
        - amount (float): Updated cost
        - category (str): Updated category
        - date (str): Updated date in YYYY-MM-DD format
        - description (str): Updated description
    
    Returns:
        GET: Rendered HTML template for the edit expense form
        POST: Redirect to index page on success with flash message
        
    Raises:
        404: If expense with given id is not found
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
    """
    Delete an expense from the database.
    
    Args:
        id (int): The unique identifier of the expense to delete
    
    Returns:
        Redirect to index page with flash message confirming deletion
        
    Raises:
        404: If expense with given id is not found
    """
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    """
    Display expense breakdown by category.
    
    Aggregates all expenses by category, calculating the total amount
    spent in each category.
    
    Returns:
        str: Rendered HTML template showing categories and their totals
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
    """
    API endpoint to retrieve all expenses as JSON.
    
    Provides a RESTful JSON API for accessing expense data. This can be used
    by external applications or for client-side JavaScript processing.
    
    Returns:
        Response: JSON array of expense objects with the following structure:
            - id (int): Expense unique identifier
            - title (str): Expense title
            - amount (float): Expense amount
            - category (str): Expense category
            - date (str): Expense date in YYYY-MM-DD format
            - description (str): Expense description (may be null)
            
    Example response:
        [
            {
                "id": 1,
                "title": "Grocery Shopping",
                "amount": 150.75,
                "category": "Food",
                "date": "2025-05-01",
                "description": "Weekly groceries"
            }
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
