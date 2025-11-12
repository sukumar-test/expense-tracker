from __future__ import division
from builtins import print
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import sys

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
    expenses = Expense.query.order_by(Expense.date.desc()).all()
    total_amount = sum(expense.amount for expense in expenses)
    return render_template('index.html', expenses=expenses, total_amount=total_amount)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            if not title:
                flash('Title is required.', 'error')
                return render_template('add.html', now=datetime.utcnow(), error=True)
                
            amount_str = request.form.get('amount')
            try:
                amount = float(amount_str)
            except ValueError:
                flash('Invalid amount', 'error')
                return render_template('add.html', now=datetime.utcnow(), error=True)
                
            category = request.form.get('category')
            if not category:
                flash('Category is required.', 'error')
                return render_template('add.html', now=datetime.utcnow(), error=True)
                
            date_str = request.form.get('date')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('add.html', now=datetime.utcnow(), error=True)
                
            description = request.form.get('description')
            
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
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'error')
            return render_template('add.html', now=datetime.utcnow(), error=True)
    
    # Pass today's date to the template
    return render_template('add.html', now=datetime.utcnow())

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    expense = Expense.query.get_or_404(id)

    if request.method == 'POST':
        try:
            title = request.form.get('title')
            if not title:
                flash('Title is required.', 'error')
                return render_template('edit.html', expense=expense, error=True)

            amount_str = request.form.get('amount')
            try:
                amount = float(amount_str)
            except ValueError:
                flash('Invalid amount', 'error')
                return render_template('edit.html', expense=expense, error=True)

            category = request.form.get('category')
            if not category:
                flash('Category is required.', 'error')
                return render_template('edit.html', expense=expense, error=True)

            date_str = request.form.get('date')
            try:
                date = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
            except ValueError:
                flash('Invalid date format', 'error')
                return render_template('edit.html', expense=expense, error=True)

            description = request.form.get('description')

            expense.title = title
            expense.amount = amount
            expense.category = category
            expense.date = date
            expense.description = description

            db.session.commit()

            flash('Expense updated successfully!', 'success')
            return redirect(url_for('index'))
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'error')
            return render_template('edit.html', expense=expense, error=True)

    return render_template('edit.html', expense=expense)

@app.route('/categories')
def categories():
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
    """Create all database tables."""
    db.create_all()

if __name__ == '__main__':
    """Run the Flask app."""
    app.run(debug=True)