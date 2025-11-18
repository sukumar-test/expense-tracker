"""Test suite for database models in the expense tracker application.

This module contains comprehensive tests for the Expense model, including
validation of model creation, database operations, field constraints, and
default value behavior.
"""
from datetime import datetime, date
from app import Expense, db

def test_expense_model(app):
    """Test the Expense model creation and database persistence.

    This test validates the complete lifecycle of an Expense model instance:
    - Creates an expense with all required and optional fields
    - Persists the expense to the database
    - Queries the database to retrieve the expense
    - Validates all field values match the input data
    - Verifies the __repr__ method returns the expected string format

    Args:
        app: Flask application fixture with application context.

    Asserts:
        - Expense is successfully created and persisted
        - All field values (title, amount, category, date, description) match
        - The __repr__ method returns '<Expense {title}>' format
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
    """Test default date assignment when no date is provided.

    This test verifies that the Expense model correctly assigns a default
    date value when an expense is created without explicitly providing a date.
    This tests the model's date field default behavior.

    Args:
        app: Flask application fixture with application context.

    Asserts:
        - An expense can be created without providing a date
        - The date field is automatically populated (not None)
        - The assigned date is a valid date object

    Note:
        The test doesn't check for a specific date value since it depends
        on when the test runs, but validates the date type and existence.
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
