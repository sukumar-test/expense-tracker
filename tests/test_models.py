"""Tests for database models in the expense tracker application.

This module contains test cases that verify the correct behavior of the
Expense model, including field validation, default values, and database operations.
"""

from datetime import datetime, date
from app import Expense, db


def test_expense_model(app):
    """Test the Expense model creation and database operations.
    
    Verifies that an Expense object can be created with all fields,
    saved to the database, and queried correctly. Also tests the
    __repr__ method.
    
    Args:
        app (Flask): The Flask application fixture with test database.
    """
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
    """Test that the Expense model uses a default date when none is provided.
    
    Verifies that when an Expense is created without specifying a date,
    the model automatically assigns a valid date value.
    
    Args:
        app (Flask): The Flask application fixture with test database.
    """
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
