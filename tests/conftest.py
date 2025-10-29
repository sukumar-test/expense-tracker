"""
Test configuration and fixtures for the Expense Tracker application.

This module sets up pytest fixtures that are used across all test modules.
It provides a test application instance with an isolated SQLite database
and sample data for testing.

Fixtures:
    app: Configured Flask application instance for testing
    client: Test client for making HTTP requests
    runner: Test CLI runner for the application
"""

import pytest
import os
import sys
import tempfile
from datetime import datetime

# Add the parent directory to sys.path to import the app
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Import here to avoid circular imports
import app as flask_app_module
from app import db, Expense

@pytest.fixture
def app():
    """
    Create and configure a Flask app for testing.
    
    Creates a temporary SQLite database for test isolation and populates it
    with sample expense data. The database is automatically cleaned up after
    each test.
    
    Sample data includes:
        - Grocery Shopping: $150.75 (Food category)
        - Electric Bill: $87.30 (Utilities category)
        - Movie Tickets: $35.50 (Entertainment category)
    
    Yields:
        Flask: Configured Flask application instance in testing mode
    """
    # Create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    
    test_app = flask_app_module.app
    test_app.config['TESTING'] = True
    test_app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    test_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    # Create the database and the tables
    with test_app.app_context():
        db.create_all()
        
        # Add some sample data
        sample_expenses = [
            Expense(
                title='Grocery Shopping', 
                amount=150.75, 
                category='Food', 
                date=datetime.strptime('2025-05-01', '%Y-%m-%d'),
                description='Weekly groceries'
            ),
            Expense(
                title='Electric Bill', 
                amount=87.30, 
                category='Utilities', 
                date=datetime.strptime('2025-05-05', '%Y-%m-%d'),
                description='Monthly electricity bill'
            ),
            Expense(
                title='Movie Tickets', 
                amount=35.50, 
                category='Entertainment', 
                date=datetime.strptime('2025-05-10', '%Y-%m-%d'),
                description='Weekend movie'
            )
        ]
        
        for expense in sample_expenses:
            db.session.add(expense)
        
        db.session.commit()
    
    yield test_app
    
    # Close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    """
    Create a test client for the app.
    
    Args:
        app: The Flask application fixture
    
    Returns:
        FlaskClient: A test client for making HTTP requests to the application
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """
    Create a test CLI runner for the app.
    
    Args:
        app: The Flask application fixture
    
    Returns:
        FlaskCliRunner: A test runner for CLI commands
    """
    return app.test_cli_runner()
