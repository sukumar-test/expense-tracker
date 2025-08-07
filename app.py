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

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    expense = Expense.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(expense)
        db.session.commit()
        flash('Expense deleted successfully!', 'success')
        return redirect(url_for('index'))
    return render_template('delete.html', expense=expense)


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

@app.route('/game')
def game():
    """Car race game page."""
    return render_template('game.html')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
