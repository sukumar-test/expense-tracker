"""Pytest configuration and shared fixtures for the expense tracker application.

This module provides pytest fixtures that are automatically discovered and made
available to all test modules in the test suite. It configures the Flask
application for testing with an isolated temporary database and provides
common test utilities.

Fixtures:
    app: A configured Flask application instance with a temporary database
    client: A Flask test client for making HTTP requests to the application
    runner: A Flask CLI test runner for testing command-line interface commands

The fixtures use pytest's dependency injection to ensure proper test isolation
and automatic cleanup of resources after each test run.
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
    """Create and configure a Flask application instance for testing.

    This fixture provides a fully configured Flask application with a temporary
    SQLite database that is isolated for each test. The database is pre-populated
    with sample expense data to facilitate testing without requiring manual setup
    in each test function.

    The fixture performs the following setup:
        1. Creates a temporary database file using tempfile.mkstemp()
        2. Configures the Flask app with test-specific settings:
           - TESTING mode enabled
           - Isolated SQLite database URI
           - CSRF protection disabled for easier testing
        3. Initializes the database schema using SQLAlchemy
        4. Populates the database with three sample expense records:
           - Grocery Shopping ($150.75, Food category, 2025-05-01)
           - Electric Bill ($87.30, Utilities category, 2025-05-05)
           - Movie Tickets ($35.50, Entertainment category, 2025-05-10)

    The fixture uses the 'yield' pattern to ensure proper cleanup. After the
    test completes, it automatically closes the database file descriptor and
    removes the temporary database file from the filesystem.

    Yields:
        Flask: A configured Flask application instance with a temporary database
            and sample data. The application context is available for the duration
            of the test.

    Example:
        def test_home_page(app, client):
            # The app fixture provides the configured Flask instance
            # The client fixture (which depends on app) provides the test client
            response = client.get('/')
            assert response.status_code == 200
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
    """Create a Flask test client for making HTTP requests to the application.

    This fixture provides a test client that can be used to make HTTP requests
    to the Flask application without running a live server. It automatically
    handles cookies and session data across requests, making it ideal for
    testing web endpoints, forms, and user workflows.

    The test client is created from the Flask app fixture, ensuring it uses
    the same isolated test database and configuration. It supports all standard
    HTTP methods (GET, POST, PUT, DELETE, etc.) and provides access to response
    data, status codes, headers, and more.

    Args:
        app: The Flask application fixture that provides the configured
            application instance with a temporary test database.

    Returns:
        FlaskClient: A test client instance that can make requests to the
            application. The client maintains session state across requests
            within a test function.

    Example:
        def test_add_expense(client):
            # Make a POST request to add a new expense
            response = client.post('/add', data={
                'title': 'Test Expense',
                'amount': '50.00',
                'category': 'Test'
            })
            assert response.status_code == 302  # Redirect after success

        def test_view_expenses(client):
            # Make a GET request to view all expenses
            response = client.get('/')
            assert b'Grocery Shopping' in response.data
    """
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a Flask CLI test runner for testing command-line commands.

    This fixture provides a CLI test runner that can be used to test Flask
    command-line interface commands without actually invoking them through
    the shell. This is useful for testing custom Flask CLI commands, such as
    database initialization commands, data import/export scripts, or any other
    CLI functionality.

    The runner captures the output of CLI commands and allows tests to verify
    both the command's exit code and its output. It uses the same isolated
    test environment as other fixtures, ensuring CLI commands operate on the
    temporary test database.

    Args:
        app: The Flask application fixture that provides the configured
            application instance with a temporary test database.

    Returns:
        FlaskCliRunner: A CLI test runner instance that can invoke Flask
            commands and capture their output. The runner provides methods
            to invoke commands and access their results.

    Example:
        def test_custom_cli_command(runner):
            # Invoke a custom Flask CLI command
            result = runner.invoke(args=['init-db'])
            assert result.exit_code == 0
            assert 'Database initialized' in result.output

        def test_database_export(runner):
            # Test a data export command
            result = runner.invoke(args=['export', '--format', 'csv'])
            assert result.exit_code == 0
            assert 'Exported' in result.output
    """
    return app.test_cli_runner()
