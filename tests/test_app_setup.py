"""Test suite for application setup and configuration.

This module contains tests to verify that the Flask application is
correctly configured and initialized, including:
- Configuration settings
- Route registration
- Application structure

All tests use pytest fixtures defined in conftest.py.
"""
import os

def test_app_config(app):
    """Test that the Flask application is configured correctly.
    
    Verifies that:
    - Testing mode is enabled
    - Database URI is configured for SQLite
    - SQLAlchemy track modifications is disabled
    - Secret key is set correctly
    
    Args:
        app (Flask): The Flask application fixture.
    """
    assert app.config['TESTING'] == True
    assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
    assert app.secret_key == 'expense_tracker_secret_key'
    
def test_app_routes_registered(app):
    """Test that all necessary routes are registered in the application.
    
    Verifies that all expected URL routes are properly registered in
    the Flask application's URL map.
    
    Routes Tested:
        - / (index)
        - /add (add expense)
        - /edit/<int:id> (edit expense)
        - /delete/<int:id> (delete expense)
        - /categories (category summary)
        - /api/expenses (API endpoint)
    
    Args:
        app (Flask): The Flask application fixture.
    """
    routes = [rule.rule for rule in app.url_map.iter_rules()]
    
    # Check that all expected routes are registered
    assert '/' in routes
    assert '/add' in routes
    assert '/edit/<int:id>' in routes
    assert '/delete/<int:id>' in routes
    assert '/categories' in routes
    assert '/api/expenses' in routes
