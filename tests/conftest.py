"""Pytest configuration and fixtures for the expense tracker tests.

This module provides pytest fixtures that set up the test environment,
including a test Flask application with an isolated database and test client.
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
    """Create and configure a Flask app for testing.
    
    Sets up a temporary database for isolated testing, configures the app
    for testing mode, and populates it with sample expense data.
    
    Yields:
        Flask: A configured Flask application instance for testing.
        
    Cleanup:
        Removes the temporary database file after tests complete.
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
    """Create a test client for the Flask app.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        FlaskClient: A test client for making requests to the app.
    """
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create a test CLI runner for the Flask app.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        FlaskCliRunner: A test CLI runner for the app.
    """
    return app.test_cli_runner()
