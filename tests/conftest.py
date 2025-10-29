"""Test configuration and fixtures for the Expense Tracker application.

This module provides pytest fixtures for testing the Flask application.
It sets up test database instances with sample data and provides test clients
for making requests to the application during testing.

The fixtures use temporary SQLite databases that are created for each test
and cleaned up afterwards to ensure test isolation.

Fixtures:
    app: Configured Flask application instance for testing.
    client: Test client for making HTTP requests to the application.
    runner: Test CLI runner for the application.
    
Example:
    To use these fixtures in tests::
    
        def test_example(client):
            response = client.get('/')
            assert response.status_code == 200
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
    """Create and configure a Flask app instance for testing.
    
    Creates a temporary SQLite database for each test to ensure isolation.
    The database is populated with sample expense data for testing purposes.
    
    Yields:
        Flask: Configured Flask application instance with test settings and sample data.
        
    Configuration:
        - TESTING: Set to True to enable test mode
        - SQLALCHEMY_DATABASE_URI: Points to a temporary SQLite database
        - WTF_CSRF_ENABLED: Disabled for easier form testing
        
    Sample Data:
        Three sample expenses are created:
        1. Grocery Shopping - $150.75 (Food category)
        2. Electric Bill - $87.30 (Utilities category)
        3. Movie Tickets - $35.50 (Entertainment category)
        
    Cleanup:
        The temporary database file is automatically deleted after the test completes.
        
    Example:
        >>> def test_with_app(app):
        ...     with app.app_context():
        ...         expenses = Expense.query.all()
        ...         assert len(expenses) == 3
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
    """Create a test client for making HTTP requests to the application.
    
    The test client can be used to make GET, POST, and other HTTP requests
    to the application routes without running a real server.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        FlaskClient: A test client for the Flask application.
        
    Example:
        >>> def test_index_page(client):
        ...     response = client.get('/')
        ...     assert response.status_code == 200
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the application.
    
    The CLI runner can be used to test Flask CLI commands.
    
    Args:
        app (Flask): The Flask application fixture.
        
    Returns:
        FlaskCliRunner: A test CLI runner for the Flask application.
        
    Example:
        >>> def test_cli_command(runner):
        ...     result = runner.invoke(args=['--help'])
        ...     assert result.exit_code == 0
    """
    return app.test_cli_runner()
