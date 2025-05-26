"""
Test file for testing database models in the expense tracker application.
"""
from datetime import datetime, date
from app import Expense, db

def test_expense_model(app):
    """Test the Expense model."""
    with app.app_context():
        # Create a new expense
        expense = Expense(
            title='Test Model',
            amount=100.00,
            category='Test',
            date=datetime.strptime('2025-05-20', '%Y-%m-%d'),
            description='Test description'
        )
        
        # Add to database
        db.session.add(expense)
        db.session.commit()
        
        # Query the database
        queried_expense = Expense.query.filter_by(title='Test Model').first()
        
        # Check that the expense was created properly
        assert queried_expense is not None
        assert queried_expense.title == 'Test Model'
        assert queried_expense.amount == 100.00
        assert queried_expense.category == 'Test'
        assert queried_expense.date == datetime.strptime('2025-05-20', '%Y-%m-%d').date()
        assert queried_expense.description == 'Test description'
        
        # Test __repr__ method
        assert repr(queried_expense) == '<Expense Test Model>'
        
def test_expense_default_date(app):
    """Test that the expense model uses default date when none is provided."""
    with app.app_context():
        # Create a new expense without a date
        expense = Expense(
            title='No Date Expense',
            amount=50.00,
            category='Test',
            description='No date provided'
        )
        
        # Add to database
        db.session.add(expense)
        db.session.commit()
        
        # Query the database
        queried_expense = Expense.query.filter_by(title='No Date Expense').first()
        
        # Check that a date was assigned
        assert queried_expense.date is not None
        # Since we don't know when the test will run, just verify it's a valid date
        assert isinstance(queried_expense.date, date)
