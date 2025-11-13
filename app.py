"""Expense Tracker Application.

This Flask web application allows users to track personal expenses by providing
features to add, edit, delete, and categorize expenses. It uses SQLite for data
storage and provides both a web interface and a REST API.

The application includes:
- CRUD operations for expenses
- Category-based expense organization
- Total expense calculation
- RESTful API endpoints
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


class Expense(db.Model):
    """Database model representing an expense entry.
    
    Attributes:
        id (int): Primary key identifier for the expense.
        title (str): Title or name of the expense (max 100 characters).
        amount (float): Monetary amount of the expense.
        category (str): Category classification for the expense (max 50 characters).
        date (date): Date when the expense occurred, defaults to current UTC date.
        description (str): Optional detailed description of the expense.
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
            str: String representation in the format '<Expense title>'.
        """
        return f'<Expense {self.title}>'


@app.route('/')
def index():
    """Display the main page with all expenses.
    
    Retrieves all expenses from the database ordered by date (most recent first)
    and calculates the total amount of all expenses.
    
    Returns:
        str: Rendered HTML template with expenses and total amount.
    """
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Add a new expense to the database.
    
    GET request displays the form to add a new expense.
    POST request processes the form data and creates a new expense entry.
    
    Returns:
        str: For GET requests, returns the rendered add expense form.
             For POST requests, redirects to the index page after adding the expense.
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
    
    GET request displays the edit form pre-populated with expense data.
    POST request updates the expense with new data.
    
    Args:
        id (int): The unique identifier of the expense to edit.
        
    Returns:
        str: For GET requests, returns the rendered edit form.
             For POST requests, redirects to the index page after updating.
             
    Raises:
        404: If the expense with the given id does not exist.
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
    
    Args:
        id (int): The unique identifier of the expense to delete.
        
    Returns:
        str: Redirects to the index page after deletion.
        
    Raises:
        404: If the expense with the given id does not exist.
    """
    expense = Expense.query.get_or_404(id)
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted successfully!', 'danger')
    return redirect(url_for('index'))

@app.route('/categories')
def categories():
    """Display expense summary grouped by categories.
    
    Aggregates all expenses by category and calculates the total amount
    spent in each category.
    
    Returns:
        str: Rendered HTML template with category summaries.
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
    """REST API endpoint to retrieve all expenses in JSON format.
    
    Returns:
        Response: JSON array containing all expenses with their details.
                 Each expense includes id, title, amount, category, date, and description.
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
